navpage<template>
	<div class="container-fluid px-3 hate" v-if="nav.show_about == true">
		<div class="fs-1 my-1">
			Author:
			<span class="text-warning">OrzOGC</span>
		</div>
		<div class="fs-1 my-1">活的精彩,修的痛快,Ford</div>
		<div class="fs-1 my-1">違規魔人都去死一死啦幹</div>
		<div class="fs-1 my-1">臉皮都比我阿嬤的腳底皮還厚啦幹</div>
		<div class="fs-1 my-1">三寶都他媽的去吃屎啦幹</div>
		<div class="fs-1 my-1">龜仔開那麼慢還不滾去騎勁戰啦幹</div>
		<div class="fs-1 my-2">他媽的南部鄉下彰化人就是沒水準啦幹</div>
		<div class="text-black lh-1 fuck fuck-1" :class="fuck_class[0]">幹</div>
		<div class="text-black lh-1 fuck fuck-2" :class="fuck_class[1]">恁</div>
		<div class="text-black lh-1 fuck fuck-3" :class="fuck_class[2]">娘</div>
		<div class="text-black lh-1 fuck fuck-4" :class="fuck_class[3]">啦</div>
	</div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { nav } from "../js/global.mjs";

let fuck_class = ref(["", "", "", ""]);
let flag = 0;
const delay = 3000;
function toggle(flag) {
	if (fuck_class.value[flag] == "") {
		fuck_class.value[flag] = "fuck-top";
	} else {
		fuck_class.value[flag] = "";
	}
}
onMounted(() => {
	setInterval(() => {
		if (nav.value.show_about == true) {
			flag = Math.round(Math.random() * 3);
			toggle(flag);
		}
	}, delay);
});
</script>

<style>
.hate {
	text-shadow: 3px 3px 5px black;
}

.fuck {
	z-index: -1;
	font-size: 500;
	font-weight: bold;
	position: absolute;
	-webkit-text-stroke: 5px orange;
	text-shadow: 20px 20px 40px black;
	transition: ease-in-out;
}

.fuck-top {
	z-index: 1000;
}

.fuck-1 {
	top: 25%;
	left: -5%;
	transform: rotate(-20deg);
}

.fuck-2 {
	top: -5%;
	left: 20%;
	transform: rotate(-5deg);
}

.fuck-3 {
	top: 25%;
	left: 45%;
	transform: rotate(10deg);
}

.fuck-4 {
	top: 5%;
	left: 70%;
	transform: rotate(25deg);
}
</style>