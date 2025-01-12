<script setup lang="ts">
import LandingTemplate from '@/components/template/LandingTemplate.vue'
import devicedp from "./devicedp.json"
</script>

<template>
    <LandingTemplate :schema="devicedp"/>
</template>