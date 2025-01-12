<script setup lang="ts">
import NwccLanding from './NwccLanding.vue'
import nwcc from "./nwcc.json"
</script>

<template>
    <NwccLanding :schema="nwcc"/>
</template>