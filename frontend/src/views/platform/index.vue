<script setup lang="ts">
import LandingTemplate from '@/components/template/LandingTemplate.vue'
import platform from "./platform.json"
</script>

<template>
    <LandingTemplate :schema="platform"/>
</template>