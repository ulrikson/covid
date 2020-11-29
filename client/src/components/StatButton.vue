<template>
    <div :class="['text-dark mx-2 py-1 px-2 rounded-3xl hover:opacity-100', bgColor, chosen ? 'opacity-100' : 'opacity-50']">{{text}}</div>
</template>

<script>
export default {
    props: ['text', 'chosen', 'bgColor']
}
</script>