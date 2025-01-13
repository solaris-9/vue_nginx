<script setup lang="ts">
import { computed } from 'vue'
import defaultSettings from "@/settings";
</script>

<template>
    <div
        class="footer"
    >
        {{ defaultSettings.version }} / Copyright ©2024
    </div>
</template>

<style lang="css" scoped>
.footer {
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    height: 30px;
    color: rgb(168, 171, 178);
    background-color: rgb(245, 247, 249);
}
</style>