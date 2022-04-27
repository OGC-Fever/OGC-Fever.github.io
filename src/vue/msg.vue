<template>
	<div v-if="nav.show_msg == true" class="txt">
		<div class="bg-dark fab text-warning fs-1 lh-1 fw-bolder text-center" type="button" @click="show_fab">+</div>
		<div class="bg-dark border border-secondary input" v-if="fab == 1">
			<div type="button" class="position-absolute top-0 end-0 btn-close btn-close-white" @click="show_fab"></div>
			<div class="row w-100 h-75 mx-auto mt-3">
				<div class="col-9">
					<div class="form-floating">
						<textarea id="input"
							class="zero text-light border-secondary bg-dark h-100 lh-base form-control txt"
							v-model="input">{{ input }}</textarea>
						<label for="input" class="text-light">{{ label }}</label>
					</div>
				</div>
				<div class="col ps-0 me-3 flex-column d-flex">
					<div type="button" class="border btn-block border-secondary rounded my-2 text-center text-success"
						@click="post">Post</div>
					<div type="button" class="border btn-block border-secondary rounded my-2 text-danger text-center"
						@click="clear">Clear</div>
					<div type="button" class="border btn-block border-secondary rounded my-2 text-warning text-center"
						@click="reset">Reset</div>
					<div type="button" class="border btn-block border-secondary text-center rounded my-2 text-info"
						@click="about">About</div>
				</div>
			</div>
			<div class="row my-2 mx-2 align-items-center">
				<div class="col-2">Author</div>
				<input class="col-5 py-2 bg-dark rounded border border-secondary text-light px-2" type="text"
					placeholder="八卦山下痣九" maxlength="50" v-model="nickname" />
			</div>
		</div>
		<div class="row h-100">
			<template v-for="rec in messages">
				<div class="col-2 h-25" :style="rec.bg" @click="hello(rec.msg, rec.nic)">
					<div class="zero text-light h-75 mt-2 overflow-auto text-break text-wrap txt lh-sm"
						v-if="rec.msg != ''">{{ rec.msg }}</div>
					<div class="zero text-light d-flex align-self-center justify-content-end fw-light small"
						v-if="rec.date != ''">{{ rec.date }}</div>
				</div>
			</template>
		</div>
	</div>
</template>

<style>
.input {
	width: 40%;
	height: 55%;
	top: 27.5%;
	left: 30%;
	border-radius: 10px;
	position: fixed;
	filter: opacity(0.95);
}

.fab {
	top: 90%;
	left: 95%;
	width: 50px;
	height: 50px;
	border-radius: 30%;
	position: fixed;
}

.txt::-webkit-scrollbar {
	display: none;
}

.zero {
	font-feature-settings: "zero";
}
</style>

<script setup>
import { ref, onMounted } from "vue";
import { nav } from "../js/global.mjs";
import { initializeApp } from 'firebase/app';
import { getDatabase, ref as gref, set, onValue, get, update } from "firebase/database";
import { initializeAppCheck, ReCaptchaV3Provider } from 'firebase/app-check';

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
const appCheck = initializeAppCheck(app, {
	provider: new ReCaptchaV3Provider('6LcBNv4dAAAAAIvtoqY-KvLMdO1rTdPFhM2uxlYW'),
});
let grid = 24

let input = ref("")
let label = ref("")
let nickname = ref("")
let messages = ref({})
let fab = ref(0)

onMounted(() => {
	init()
});

function hello(text, nic) {
	fab.value = 1
	label.value = "message"
	input.value = text
	nickname.value = nic
}


function show_fab() {
	if (fab.value == 0) {
		fab.value = 1
	} else {
		fab.value = 0
	}
}

function random_bg() {
	let h = Math.ceil(Math.random() * 360)
	let s = Math.ceil(Math.random() * 75) + 25
	let l = Math.ceil(Math.random() * 25) + 5
	return (`background-color:hsla(${h},${s}%,${l}%)`)
}

function read(index) {
	onValue(gref(db, `/msg/${index}`), (e) => {
		let data = e.val()
		try {
			messages.value[index] = { msg: data.msg, date: data.date, bg: data.bg, nic: data.nic }
		} catch (error) {
			messages.value[index] = { msg: "", date: "", bg: random_bg(), nic: "" }
		}
	});
}

function about() {
	let about = `author: OrzOGC
	non-professional developer
	senior mechanical designer
	senior part-time gofer
	and road rage monster`
	input.value = about
	label.value = "about"
	nickname.value = "OrzOGC"
}

function init() {
	clear()
	for (let index = 1; index <= grid; index++) {
		read(index)
	}
}

function post() {
	let msg = input.value
	let id
	let nic = nickname.value
	if (nic == null) {
		nic = ""
	}
	if (msg == "") {
		label.value = "Oops!"
	}
	if (msg != "") {
		get(gref(db, "/msg/flag")).then((e) => {
			let flag = e.val()
			if (flag >= grid) {
				id = 1
			} else {
				id = flag + 1;
			}
			let options = {
				day: 'numeric',
				month: 'short',
				year: 'numeric',
				hour: '2-digit',
				minute: '2-digit',
				hour12: false,
			};
			set(gref(db, `/msg/${id}`), {
				msg: msg,
				date: new Date().toLocaleString('en-US', options),
				bg: random_bg(),
				nic: nic
			});
			update(gref(db, '/msg/'), {
				flag: id,
			})
			init()
			fab.value = 0
		})
	}
}

function clear() {
	input.value = ""
	label.value = "Write some messages"
	nickname.value = ""
}

function reset() {
	for (let index = 1; index <= grid; index++) {
		update(gref(db, `/msg/${index}`), {
			bg: random_bg(),
		})
	}
	clear()
}
</script>
