<script setup lang="ts">
import LandingTemplate from '@/components/template/LandingTemplate.vue'
import grade from "./grade.json"
</script>

<template>
    <LandingTemplate :schema="grade"/>
</template>