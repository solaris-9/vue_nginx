<script setup lang="js">

// Props
const props = defineProps({
    form: {
        type: Object,
        required: true
    },
    fields: {
        type: Array,
        required: true
    },
    disabledFields: {  // New Prop for Disabled State
        type: Object,
        required: true
    }
});

</script>

<template>
    <div class="multi-input">
    <template v-for="field in fields" :key="field.model">
        <el-input 
            v-model="form[field.model]"
            type="text"
            :placeholder="field.label"
            :disabled="disabledFields[field.model]"
        />
    </template>
    </div>
</template>

<style lang="css">
.multi-input {
    display: flex;
    flex-direction: column;
    gap: 5px;
    width: 100%;

}
</style>