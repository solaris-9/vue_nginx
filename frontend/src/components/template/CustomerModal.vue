<script setup lang="ts">
import { reactive, ref, watch, onMounted, computed } from "vue";
import SimpleFormTemplate from "./SimpleFormTemplate.vue"
import schema from "@/views/customer/customer.json"
</script>

<template>
    <SimpleFormTemplate schema="schema" />
</template>