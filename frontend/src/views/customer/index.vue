<script setup lang="ts">
import LandingTemplate from '@/components/template/LandingTemplate.vue'
import customer from "./customer.json"
</script>

<template>
    <LandingTemplate :schema="customer"/>
</template>