<template>
  <div class="relative mx-auto flex h-dvh w-full max-w-[402px] flex-col overflow-hidden bg-white">
    <slot name="header" />
    <div class="flex min-h-0 flex-1 flex-col overflow-y-auto">
      <slot />
    </div>
    <slot name="fab" />
    <slot name="footer" />
  </div>
</template>
