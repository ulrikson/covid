<template>
    <div :class="['text-dark mx-2 py-1 px-2 rounded-3xl hover:opacity-50', bgColor, chosen ? 'opacity-50' : 'chosen-80']">{{text}}</div>
</template>

<script>
export default {
    props: ['text', 'chosen', 'bgColor']
}
</script>