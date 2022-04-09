navpage<template>
	<div class="row me-auto" v-show="nav.show_map == true">
		<div class="col-8 mt-1 ps-1">
			<div id="map"></div>
		</div>
		<div class="col-4 ps-0 pe-2">
			<div class="row offset-3 my-2 ps-0">Adding SanBau Data</div>
			<div class="row align-items-center mb-1">
				<div class="col-3 ps-2">Nickname</div>
				<input
					class="col rounded border py-2 bg-dark text-light"
					type="text"
					placeholder="300哥/祭央乂/馬維拉/韓總機"
					v-model="data.nickname"
					maxlength="20"
				/>
			</div>
			<div class="row align-items-center mb-1">
				<div class="col-3 ps-2">Plate</div>
				<input
					class="col rounded border py-2 bg-dark text-light me-1"
					type="text"
					placeholder="ABC-1234"
					v-model="data.plate"
				/>
				<select
					class="col-4 py-2 rounded border bg-dark text-light"
					v-model="data.type"
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
				<input class="col border rounded py-2 me-1 bg-dark text-light" v-model="data.date" type="date" />
				<input class="col-4 border rounded py-2 bg-dark text-light" v-model="data.time" type="time" />
			</div>

			<div class="row align-items-center mb-1">
				<div class="col-3 ps-2">Behavior</div>
				<textarea
					class="col py-2 border rounded bg-dark text-light"
					type="text"
					placeholder="How SanBau?"
					maxlength="100"
					v-model="data.behavior"
				></textarea>
			</div>
			<div class="row align-items-center mb-1">
				<div class="col-3 ps-2">Address</div>
				<textarea
					class="col py-2 border rounded bg-dark text-light"
					type="text"
					placeholder="Where? (option)"
					maxlength="100"
					v-model="data.address"
				></textarea>
			</div>
			<div class="row align-items-center mb-1">
				<div class="col-3 ps-2">Lat, Lng</div>
				<input
					class="col border rounded bg-dark text-light py-2"
					type="text"
					placeholder="Location"
					v-model="data.latlng"
					maxlength="30"
				/>
				<div class="badge col-2 text-warning" type="button" @click="get_location">
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
					class="col border rounded py-2 bg-dark text-secondary"
					type="url"
					placeholder="upload image/video"
					v-model="data.link"
					@click="open_link"
				/>
				<div class="col-2" @click="upload" type="button">
					<img class="w-100" src="https://s.imgur.com/images/favicon.png" />
				</div>
			</div>
			<div class="row mt-2 justify-content-center">
				<div class="col-3 badge fs-6 border text-success me-1 ms-1 py-2" type="button" @click="add">Add</div>
				<div class="col-3 badge fs-6 border text-danger py-2" type="button" @click="clear">Clear</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { nav } from "../js/global.mjs";
import { ref, onMounted } from "vue";
import L from "leaflet";

let map, lat, lng, marker_point;
let marker = L.marker();
let data = ref({ type: "car" });
let roundto = 7;

function get_location() {
	map.setView([lat, lng]);
	data.value.latlng = `${lat.toFixed(roundto)}, ${lng.toFixed(roundto)}`;
	map.removeLayer(marker);
	L.marker([lat, lng]).addTo(map).bindPopup("you're here").openPopup();
}

function upload() {
	window.open("https://imgur.com/upload");
}

function add() {
	clear();
}

function open_link() {
	if (data.value.link != "" && data.value.link != null) {
		if (confirm("open link in new window?")) {
			window.open(data.value.link);
		}
	}
}

function clear() {
	data.value = [];
	data.value.type = "car";
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
	let type = data.value.type;
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
	data.value.latlng = `${point.latlng.lat.toFixed(
		roundto
	)}, ${point.latlng.lng.toFixed(roundto)}`;
}

function change_type() {
	let type = data.value.type;
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
					data.value.link = clipText;
				} else {
					data.value.link = "";
				}
			}
		} catch (error) {
			data.value.link = "";
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
