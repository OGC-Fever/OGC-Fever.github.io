<template>
	<div class="row me-auto" v-show="nav.show_map == true">
		<div class="col-8 mt-1 ps-1">
			<div id="map"></div>
		</div>
		<div class="col-4 ps-0 pe-2" v-if="nav.show_search == false">
			<div class="row offset-3 my-1 ps-0 badge">Adding SanBau Data</div>
			<div class="row align-items-center mb-1">
				<div class="col-3 ps-2">Nickname</div>
				<input class="col rounded border py-2 bg-dark text-light border-secondary" type="text"
					placeholder="C300哥/祭央乂/馬維拉/韓總機" v-model="input.nickname" maxlength="20" />
			</div>
			<div class="row align-items-center mb-1">
				<div class="col-3 ps-2">Plate</div>
				<input class="col rounded border py-2 bg-dark border-secondary text-light me-1 text-uppercase"
					type="text" placeholder="ABC-1234" v-model="input.plate" />
				<select class="col-4 py-2 rounded border-secondary border bg-dark text-light" v-model="input.type"
					@change="set_marker">
					<option value="human">Human</option>
					<option value="car">Car</option>
					<option value="motor">Motorcycle</option>
					<option value="truck">Truck</option>
				</select>
			</div>
			<div class="row align-items-center mb-1">
				<div class="col-3 ps-2">Date/Time</div>
				<input class="col border rounded py-2 me-1 bg-dark text-light border-secondary" v-model="input.date"
					type="date" />
				<input class="border-secondary col-4 border rounded py-2 bg-dark text-light" v-model="input.time"
					type="time" />
			</div>

			<div class="row align-items-center mb-1">
				<div class="col-3 ps-2">Behavior</div>
				<textarea class="col py-2 border rounded bg-dark text-light border-secondary" type="text"
					placeholder="How SanBau?" maxlength="100" v-model="input.behavior"></textarea>
			</div>
			<div class="row align-items-center mb-1">
				<div class="col-3 ps-2">Address</div>
				<textarea class="col py-2 border rounded bg-dark text-light border-secondary" type="text"
					placeholder="Where? (option)" maxlength="100" v-model="input.address"></textarea>
			</div>
			<div class="row align-items-center mb-1">
				<div class="col-3 ps-2">Lat, Lng</div>
				<input class="col border rounded bg-dark text-light py-2 border-secondary" type="text"
					placeholder="Location" v-model="input.latlng" maxlength="30" />
				<div class="badge col-2 text-warning" title="get currten latlng" type="button" @click="get_location">
					<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor"
						class="bi bi-geo-alt" viewBox="0 0 16 16">
						<path
							d="M12.166 8.94c-.524 1.062-1.234 2.12-1.96 3.07A31.493 31.493 0 0 1 8 14.58a31.481 31.481 0 0 1-2.206-2.57c-.726-.95-1.436-2.008-1.96-3.07C3.304 7.867 3 6.862 3 6a5 5 0 0 1 10 0c0 .862-.305 1.867-.834 2.94zM8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10z" />
						<path d="M8 8a2 2 0 1 1 0-4 2 2 0 0 1 0 4zm0 1a3 3 0 1 0 0-6 3 3 0 0 0 0 6z" />
					</svg>
				</div>
			</div>
			<div class="row align-items-center mb-1">
				<div class="col-3 ps-2">appendix</div>
				<input class="col border border-secondary rounded py-2 bg-dark text-secondary" type="url"
					placeholder="Imgur Url (option)" v-model="input.link">
				<figure class="figure col-2 my-0 py-0 text-center">
					<img class="img-fluid" @click="upload" type="button" title="link to imgur"
						src="https://s.imgur.com/images/favicon.png" />
				</figure>
			</div>
			<div class="row align-items-center">
				<div class="col-3 ps-2">News</div>
				<input class="col border border-secondary rounded py-2 bg-dark text-secondary" type="url"
					placeholder="News Link (option)" v-model="input.news">
			</div>
			<div class="row mt-1 justify-content-center">
				<div class="col-3 badge fs-6 border border-secondary text-success me-1 ms-1 py-1" type="button"
					@click="post">Add</div>
				<div class="col-3 badge fs-6 border border-secondary text-danger py-1" type="button" @click="clear">
					Clear</div>
			</div>
		</div>
		<div class="col-4 px-1 my-1 " v-if="nav.show_search == true">
			<div class="row">
				<div class="fs-1 text-center" v-if="searchList.length == 0">
					~no data~
				</div>
				<table class="table table-hover table-sm" v-if="searchList.length != 0">
					<thead>
						<tr>
							<th class="col-3">Plate</th>
							<th class="col-4">Nickname</th>
							<th class="col">Date/Time</th>
						</tr>
					</thead>
					<tbody>
						<template v-for="el in searchList">
							<tr @click="popup(el)">
								<td>{{ el.plate }}</td>
								<td>{{ el.nickname }}</td>
								<td>{{ el.date }}-{{ el.time }}</td>
							</tr>
						</template>
					</tbody>
				</table>
			</div>
		</div>
	</div>
</template>

<style>
#map {
	height: 91vh;
	filter: brightness(.7) contrast(2) saturate(.5);
}

.leaflet-popup-tip,
.leaflet-popup-content-wrapper {
	background-color: black;
	opacity: .75;
}

.leaflet-popup-content {
	color: whitesmoke;
	font-size: medium;
	margin: 10px;
	width: max-content;
}
</style>

<script setup>
import { initializeApp } from 'firebase/app';
import { getDatabase, ref as gref, set, get, update, query, equalTo, startAt, orderByChild, } from "firebase/database";
import { initializeAppCheck, ReCaptchaV3Provider } from 'firebase/app-check';
import { nav, search } from "../js/global.mjs";
import { ref, onMounted, watch } from "vue";
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
const db = getDatabase(app);
// const appCheck =
initializeAppCheck(app, {
	provider: new ReCaptchaV3Provider('6LcBNv4dAAAAAIvtoqY-KvLMdO1rTdPFhM2uxlYW'),
});

let map, lat, lng, marker_point, center_coord;
let marker = L.marker();
let your_marker = L.marker();
let bau_bau_marker = L.layerGroup()
let input = ref({ type: "car" });
let roundto = 7;
let searchList = ref([])


async function post() {
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
		appendix: input.value.appendix,
		news: input.value.news
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
	let count = await get(gref(db, "/map"))
	try {
		count = Object.keys(count.val()).length
		id = count + 1
	} catch (e) {
		count = 0
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
		appendix: data.appendix,
		news: data.news
	});
	clear()
	await read()
}

function get_location() {
	navigator.geolocation.getCurrentPosition((location) => {
		lat = location.coords.latitude;
		lng = location.coords.longitude;
	})
	map.setView([lat, lng], 10);
	map.removeLayer(your_marker);
	input.value.latlng = `${lat.toFixed(roundto)}, ${lng.toFixed(roundto)}`;
	your_marker = L.marker([lat, lng]).addTo(map).bindPopup("you're here").openPopup();
	map_centered()
}

function upload() {
	window.open("https://imgur.com/upload");
}

function clear() {
	input.value = [];
	input.value.type = "car";
	map.removeLayer(marker);
}

async function map_init() {
	if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(async (location) => {
			lat = location.coords.latitude;
			lng = location.coords.longitude;
			map = L.map("map", {
				center: [lat, lng],
				zoom: 10,
				attributionControl: true,
				zoomControl: true,
			});
			L.tileLayer(
				"https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
			).addTo(map);
			your_marker = L.marker([lat, lng])
				.addTo(map)
				.bindPopup("you're here")
				.openPopup();
			await map_centered()
			map.on("click", mouse_click);
			map.on("moveend", map_centered)
		});
	}
}

async function map_centered() {
	map.removeLayer(bau_bau_marker)
	center_coord = await map.getCenter()
	bau_bau_marker = L.layerGroup().addTo(map)
	await read()
}

function mouse_click(point) {
	nav.value.show_search = false
	marker_point = point;
	set_marker()
	input.value.latlng = `${point.latlng.lat.toFixed(roundto)}, ${point.latlng.lng.toFixed(roundto)}`;
}

function set_marker() {
	let type = input.value.type;
	map.removeLayer(marker);
	marker = L.marker(marker_point.latlng, { icon: map_icon(type) })
		.addTo(map)
		.bindPopup("SamBao is here")
		.openPopup();
}

function map_icon(element) {
	let icon = L.icon({
		iconUrl: `./pic/${element}.png`,
		iconSize: [40, 40],
		popupAnchor: [0, -15],
	});
	return icon
}

async function read() {
	let count = await get(gref(db, "/map"))
	try {
		count = Object.keys(count.val()).length
	} catch (error) {
		count = 0
		return
	}
	let tag = []
	for (let index = 1; index <= count; index++) {
		let tmp = await get(gref(db, `/map/${index}`))
		tag.push(tmp.val())
	}
	tag.forEach(element => {
		let dist = L.latLng(element.latlng.split(",")).distanceTo(center_coord) / 1000
		if (dist <= 50) {
			L.marker(element.latlng.split(","), { icon: map_icon(element.type) })
				.addTo(bau_bau_marker).bindPopup(popup_html(element));
		}
	});
}

async function mock_data() {
	function ran() {
		let type = ["human", "car", "motor", "truck"]
		let flag = Math.round(Math.random() * 3);
		return type[flag]
	}
	function latlng() {
		let lat = (Math.random() * 3) + 22;
		let lng = (Math.random() * 2) + 120;
		return `${lat}, ${lng}`
	}
	for (let index = 1; index <= 100; index++) {
		set(gref(db, `/map/${index}`), {
			nickname: `name-${index}`,
			plate: `ABC-${index}`,
			type: ran(),
			behavior: `bbb-${index}`,
			address: `nnn-${index}`,
			date: "2022/2/2",
			time: "44:44:44",
			latlng: latlng(),
			appendix: "nnn",
			news: "nnn"
		});
	}
}

onMounted(async () => {
	// mock_data()
	await map_init();
});

function popup_html(e) {
	let html = `<div class="row row-cols-2">`
	if (e.nickname != "") {
		html += `<div class="col-4">Nickname</div><div class="col">${e.nickname}</div>`
	}
	if (e.plate != "") {
		html += `<div class="col-4">Plate</div><div class="col">${e.plate}</div>`
	}
	if (e.date != "") {
		html += `<div  class="col-4">Date</div><div class="col">${e.date}</div>`
	}
	if (e.time != "") {
		html += `<div class="col-4">Time</div><div class="col">${e.time}</div>`
	}
	if (e.behavior != "") {
		html += `<div class="col-4">Behavior</div><div class="col">${e.behavior}</div>`
	}
	if (e.address != "") {
		html += `<div class="col-4">Address</div><div class="col">${e.address}</div>`
	}
	if (e.appendix != "") {
		html += `<div class="col-4">Imgur</div><div class="col"><a class="text-warning fw-bold" href=${e.appendix} target="_blank">Imgur Link</a></div>`
	}
	if (e.news != "") {
		html += `<div class="col-4">News</div><div class="col"><a class="text-warning fw-bold" href=${e.news} target="_blank">News Link</a></div>`
	}
	html += `</div>`
	return html
}

function popup(e) {
	let latlng = e.latlng.split(",")
	map.setView(latlng, 10);
	map_centered()
	L.popup({ offset: L.point(0, -15) }).setLatLng(latlng).setContent(popup_html(e)).openOn(map);
}

watch(
	() => search.value,
	async (newValue, _) => {
		if (newValue != "") {
			searchList.value = [];
			let queryPlate = query(gref(db, "/map"), orderByChild("plate"), equalTo(search.value));
			let tmp1 = await get(queryPlate);
			let queryNickname = query(gref(db, "/map"), orderByChild("nickname"), equalTo(search.value));
			let tmp2 = await get(queryNickname);
			tmp1.forEach((el) => {
				if (el.val() != null) {
					searchList.value.push(el.val());
				}
			});
			tmp2.forEach(ele => {
				if (ele.val() != null) {
					searchList.value.push(ele.val());
				}
			});
			console.log(searchList.value.length);
		}
	}
)
</script>
