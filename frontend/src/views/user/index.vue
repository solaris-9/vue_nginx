<script setup lang="ts">
import LandingTemplate from '@/components/template/LandingTemplate.vue'
import user from "./user.json"
</script>

<template>
    <LandingTemplate :schema="user"/>
</template>