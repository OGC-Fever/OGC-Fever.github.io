<template>
	<div class="container-fluid d-flex pe-0 navtxt">
		<div class="navbar-brand text-light" type="button" @click="map">Cyber Butchers</div>
		<div class="navbar-brand fs-6" :class="text_class.map" type="button" @click="map">SanBau Map
		</div>
		<div class="navbar-brand fs-6" type="button" :class="text_class.about" @click="about">About</div>
		<div class="navbar-brand fs-6" type="button" :class="text_class.msg" @click="msg">Message Board</div>
		<div class="navbar-brand fs-6" type="button" @click="github">GitHub</div>
		<div class="d-flex col-4 my-1 ms-auto">
			<div class="col-4 align-self-center text-light">Finding SanBau</div>
			<input class="col-6 px-2 my-1 border border-secondary rounded bg-dark text-light" type="text"
				placeholder="Plate/Nickname" maxlength="20" v-model="search" />
			<div class="col fs-4 px-0 badge align-self-center text-warning" type="button" @click="go">Go</div>
		</div>
	</div>
</template>

<style>
.navtxt {
	text-shadow: 3px 3px 5px black;
}
</style>

<script setup>
import { ref, onMounted } from "vue";
import { nav, search } from "../js/global.mjs";

let text_class = ref({
	map: "",
	about: "",
	msg: "",
});

function nav_page(page) {
	for (let key in nav.value) {
		nav.value[key] = false;
	}
	for (let key in text_class.value) {
		text_class.value[key] = "";
	}
	nav.value[`show_${page}`] = true;
	text_class.value[page] = "text-warning";
}

function map() {
	nav_page("map");
}

function about() {
	nav_page("about");
}

function msg() {
	nav_page("msg");
}

function github() {
	window.open("https://github.com/OGC-Fever");
}

function go() {
	if (search.value == "" || search.value == null) {
		return
	} else {
		map()
		nav.value.show_search = true
	}
}

onMounted(() => {
	map();
	// about();
	// msg();
});
</script>
