<template>
	<div class="row me-auto" v-show="nav.show_map == true">
		<div class="col-8 mt-1 ps-1">
			<div id="map"></div>
		</div>
		<div class="col-4 ps-0 pe-2">
			<div class="row offset-3 my-2 ps-0">Adding SanBau Data</div>
			<div class="row align-items-center mb-1">
				<div class="col-3 ps-2">Nickname</div>
				<input
					class="col rounded border py-2 bg-dark text-light border-secondary"
					type="text"
					placeholder="300哥/祭央乂/馬維拉/韓總機"
					v-model="input.nickname"
					maxlength="20"
				/>
			</div>
			<div class="row align-items-center mb-1">
				<div class="col-3 ps-2">Plate</div>
				<input
					class="col rounded border py-2 bg-dark border-secondary text-light me-1"
					type="text"
					placeholder="ABC-1234"
					v-model="input.plate"
				/>
				<select
					class="col-4 py-2 rounded border-secondary border bg-dark text-light"
					v-model="input.type"
					@change="change_type"
				>
					<option value="human">Human</option>
					<option value="car">Car</option>
					<option value="motor">Motorcycle</option>
					<option value="truck">Truck</option>
				</select>
			</div>
			<div class="row align-items-center mb-1">
				<div class="col-3 ps-2">Date/Time</div>
				<input
					class="col border rounded py-2 me-1 bg-dark text-light border-secondary"
					v-model="input.date"
					type="date"
				/>
				<input
					class="border-secondary col-4 border rounded py-2 bg-dark text-light"
					v-model="input.time"
					type="time"
				/>
			</div>

			<div class="row align-items-center mb-1">
				<div class="col-3 ps-2">Behavior</div>
				<textarea
					class="col py-2 border rounded bg-dark text-light border-secondary"
					type="text"
					placeholder="How SanBau?"
					maxlength="100"
					v-model="input.behavior"
				></textarea>
			</div>
			<div class="row align-items-center mb-1">
				<div class="col-3 ps-2">Address</div>
				<textarea
					class="col py-2 border rounded bg-dark text-light border-secondary"
					type="text"
					placeholder="Where? (option)"
					maxlength="100"
					v-model="input.address"
				></textarea>
			</div>
			<div class="row align-items-center mb-1">
				<div class="col-3 ps-2">Lat, Lng</div>
				<input
					class="col border rounded bg-dark text-light py-2 border-secondary"
					type="text"
					placeholder="Location"
					v-model="input.latlng"
					maxlength="30"
				/>
				<div
					class="badge col-2 text-warning"
					title="get currten latlng"
					type="button"
					@click="get_location"
				>
					<svg
						xmlns="http://www.w3.org/2000/svg"
						width="32"
						height="32"
						fill="currentColor"
						class="bi bi-geo-alt"
						viewBox="0 0 16 16"
					>
						<path
							d="M12.166 8.94c-.524 1.062-1.234 2.12-1.96 3.07A31.493 31.493 0 0 1 8 14.58a31.481 31.481 0 0 1-2.206-2.57c-.726-.95-1.436-2.008-1.96-3.07C3.304 7.867 3 6.862 3 6a5 5 0 0 1 10 0c0 .862-.305 1.867-.834 2.94zM8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10z"
						/>
						<path d="M8 8a2 2 0 1 1 0-4 2 2 0 0 1 0 4zm0 1a3 3 0 1 0 0-6 3 3 0 0 0 0 6z" />
					</svg>
				</div>
			</div>
			<div class="row align-items-center">
				<div class="col-3 ps-2">appendix</div>
				<input
					class="col border border-secondary rounded py-2 bg-dark text-secondary"
					type="url"
					placeholder="upload image/video"
					v-model="input.link"
					@click="open_link"
				/>
				<div class="col-2" @click="upload" type="button" title="link to imgur">
					<img class="w-100" src="https://s.imgur.com/images/favicon.png" />
				</div>
			</div>
			<div class="row mt-2 justify-content-center">
				<div
					class="col-3 badge fs-6 border border-secondary text-success me-1 ms-1 py-2"
					type="button"
					@click="post"
				>Add</div>
				<div
					class="col-3 badge fs-6 border border-secondary text-danger py-2"
					type="button"
					@click="clear"
				>Clear</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { initializeApp } from 'firebase/app';
// import { getAnalytics } from "firebase/analytics";
import { getDatabase, ref as gref, set, onValue, get, child, update } from "firebase/database";
import { initializeAppCheck, ReCaptchaV3Provider } from 'firebase/app-check';
import { nav } from "../js/global.mjs";
import { ref, onMounted } from "vue";
import L from "leaflet";

const firebaseConfig = {
	apiKey: "AIzaSyAEvJzElQdmOL_8buY2qFP2A95inwU0Aug",
	authDomain: "cyber-butchers.firebaseapp.com",
	databaseURL:
		"https://cyber-butchers-default-rtdb.asia-southeast1.firebasedatabase.app",
	projectId: "cyber-butchers",
	storageBucket: "cyber-butchers.appspot.com",
	messagingSenderId: "904143225733",
	appId: "1:904143225733:web:3d16dd6d240892a5a5baec",
	measurementId: "G-QBBG1SGW3K"
};
const app = initializeApp(firebaseConfig);
// const analytics = getAnalytics(app);
const db = getDatabase(app);
const appCheck = initializeAppCheck(app, {
	provider: new ReCaptchaV3Provider('6LcBNv4dAAAAAIvtoqY-KvLMdO1rTdPFhM2uxlYW'),
});

let map, lat, lng, marker_point;
let marker = L.marker();
let input = ref({ type: "car" });
let roundto = 7;

function read(index) {
	onValue(gref(db, `/map/${index}`), (e) => {
		let data = e.val();
		try {
			messages.value[index] = { msg: data.msg, date: data.date, bg: data.bg, nic: data.nic };
		} catch (error) {
			messages.value[index] = { msg: "", date: "", bg: random_bg(), nic: "" };
		}
	});
}

function post() {
	let id
	let data = {
		nickname: input.value.nickname,
		plate: input.value.plate,
		type: input.value.type,
		date: input.value.date,
		time: input.value.time,
		behavior: input.value.behavior,
		address: input.value.address,
		latlng: input.value.latlng,
		appendix: input.value.appendix
	}
	if (data.nickname == null || data.plate == null || data.date == null || data.time == null || data.behavior == null || data.latlng == null) {
		return
	}
	if (data.plate != null && data.type == "human") {
		return
	}
	for (let key in data) {
		if (data[key] == null) {
			data[key] = ""
		}
	}
	get(gref(db, "/map/count")).then((e) => {
		try {
			id = e.val() + 1
		} catch (error) {
			id = 1
		}
		set(gref(db, `/map/${id}`), {
			nickname: data.nickname,
			plate: data.plate,
			type: data.type,
			behavior: data.behavior,
			address: data.address,
			date: data.date,
			time: data.time,
			latlng: data.latlng,
			appendix: data.appendix
		});
		update(gref(db, '/map/'), {
			count: id,
		})
	})
	clear()
}

function get_location() {
	map.setView([lat, lng]);
	input.value.latlng = `${lat.toFixed(roundto)}, ${lng.toFixed(roundto)}`;
	map.removeLayer(marker);
	L.marker([lat, lng]).addTo(map).bindPopup("you're here").openPopup();
}

function upload() {
	window.open("https://imgur.com/upload");
}

function open_link() {
	if (input.value.link != "" && input.value.link != null) {
		if (confirm("open link in new window?")) {
			window.open(input.value.link);
		}
	}
}

function clear() {
	input.value = [];
	input.value.type = "car";
	map.removeLayer(marker);
}

function map_init() {
	if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition((location) => {
			lat = location.coords.latitude;
			lng = location.coords.longitude;
			map = L.map("map", {
				center: [lat, lng],
				zoom: 15,
				attributionControl: true,
				zoomControl: true,
			});
			L.tileLayer(
				"https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
			).addTo(map);
			L.marker([lat, lng])
				.addTo(map)
				.bindPopup("you're here")
				.openPopup();
			map.on("click", mouse_click);
			// map.on("mouseup", test)
			// alert(map.getCenter())
		});
	}
}

// let tag = [
//     { plate: "test1", location: [24.51, 121.1] },
//     { plate: "test2", location: [24.11, 121.1] },
// ];
// let html = "<div>fuck</div>";
// tag.forEach(element => {
//     L.marker(element.location).addTo(this.map).bindPopup(element.plate + html);
// });
// });
// }
// }

function mouse_click(point) {
	marker_point = point;
	let type = input.value.type;
	let icon = L.icon({
		iconUrl: `./pic/${type}.png`,
		iconSize: [40, 40],
		popupAnchor: [0, -10],
	});
	let roundto = 7;
	map.removeLayer(marker);
	marker = L.marker(point.latlng, { icon: icon })
		.addTo(map)
		.bindPopup("SamBao is here")
		.openPopup();
	input.value.latlng = `${point.latlng.lat.toFixed(
		roundto
	)}, ${point.latlng.lng.toFixed(roundto)}`;
}

function change_type() {
	let type = input.value.type;
	let icon = L.icon({
		iconUrl: `./pic/${type}.png`,
		iconSize: [40, 40],
		popupAnchor: [0, -10],
	});
	map.removeLayer(marker);
	marker = L.marker(marker_point.latlng, { icon: icon })
		.addTo(map)
		.bindPopup("SamBao is here")
		.openPopup();
}

function paste_url() {
	navigator.clipboard.readText().then(async (clipText) => {
		try {
			if (clipText.length > 1) {
				let resp = await fetch(clipText, { mode: "no-cors" });
				if (resp.status != 404) {
					input.value.link = clipText;
				} else {
					input.value.link = "";
				}
			}
		} catch (error) {
			input.value.link = "";
		}
	});
}

onMounted(() => {
	map_init();
	if (nav.value.show_map) {
		window.addEventListener("focus", paste_url);
	}
});
</script>
