import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { ScheduleEntry } from '@/components/tab01-dashboard/ScheduleTable.vue'

export const useScheduleStore = defineStore('schedule', () => {
  const entries = ref<ScheduleEntry[]>([
    // 平日：一三五復健、二四日照中心，作息共同的起床/服藥/三餐/散步
    { day: 'mon', hour: 7, activity: '起床盥洗' },
    { day: 'mon', hour: 8, activity: '早餐服藥' },
    { day: 'mon', hour: 9, activity: '量血壓' },
    { day: 'mon', hour: 10, activity: '復健運動' },
    { day: 'mon', hour: 12, activity: '午餐' },
    { day: 'mon', hour: 13, activity: '午休' },
    { day: 'mon', hour: 15, activity: '點心時間' },
    { day: 'mon', hour: 16, activity: '散步' },
    { day: 'mon', hour: 18, activity: '晚餐服藥' },
    { day: 'mon', hour: 20, activity: '陪伴看電視' },

    { day: 'tue', hour: 7, activity: '起床盥洗' },
    { day: 'tue', hour: 8, activity: '早餐服藥' },
    { day: 'tue', hour: 9, activity: '量血壓' },
    { day: 'tue', hour: 10, activity: '社區日照中心' },
    { day: 'tue', hour: 12, activity: '午餐' },
    { day: 'tue', hour: 13, activity: '午休' },
    { day: 'tue', hour: 15, activity: '點心時間' },
    { day: 'tue', hour: 17, activity: '接回家休息' },
    { day: 'tue', hour: 18, activity: '晚餐服藥' },
    { day: 'tue', hour: 20, activity: '陪伴看電視' },

    { day: 'wed', hour: 7, activity: '起床盥洗' },
    { day: 'wed', hour: 8, activity: '早餐服藥' },
    { day: 'wed', hour: 9, activity: '量血壓' },
    { day: 'wed', hour: 10, activity: '復健運動' },
    { day: 'wed', hour: 12, activity: '午餐' },
    { day: 'wed', hour: 13, activity: '午休' },
    { day: 'wed', hour: 15, activity: '點心時間' },
    { day: 'wed', hour: 16, activity: '散步' },
    { day: 'wed', hour: 18, activity: '晚餐服藥' },
    { day: 'wed', hour: 20, activity: '陪伴看電視' },

    { day: 'thu', hour: 7, activity: '起床盥洗' },
    { day: 'thu', hour: 8, activity: '早餐服藥' },
    { day: 'thu', hour: 9, activity: '量血壓' },
    { day: 'thu', hour: 10, activity: '社區日照中心' },
    { day: 'thu', hour: 12, activity: '午餐' },
    { day: 'thu', hour: 13, activity: '午休' },
    { day: 'thu', hour: 15, activity: '點心時間' },
    { day: 'thu', hour: 17, activity: '接回家休息' },
    { day: 'thu', hour: 18, activity: '晚餐服藥' },
    { day: 'thu', hour: 20, activity: '陪伴看電視' },

    { day: 'fri', hour: 7, activity: '起床盥洗' },
    { day: 'fri', hour: 8, activity: '早餐服藥' },
    { day: 'fri', hour: 9, activity: '量血壓' },
    { day: 'fri', hour: 10, activity: '復健運動' },
    { day: 'fri', hour: 12, activity: '午餐' },
    { day: 'fri', hour: 13, activity: '公廟拜拜' },
    { day: 'fri', hour: 14, activity: '公廟拜拜' },
    { day: 'fri', hour: 16, activity: '散步' },
    { day: 'fri', hour: 18, activity: '晚餐服藥' },
    { day: 'fri', hour: 20, activity: '陪伴看電視' },

    // 周末：作息較晚起、安排家人來訪，沒有日照中心/復健課
    { day: 'sat', hour: 8, activity: '起床盥洗' },
    { day: 'sat', hour: 9, activity: '早餐服藥' },
    { day: 'sat', hour: 10, activity: '公廟拜拜' },
    { day: 'sat', hour: 12, activity: '午餐' },
    { day: 'sat', hour: 14, activity: '家人來訪' },
    { day: 'sat', hour: 16, activity: '散步' },
    { day: 'sat', hour: 18, activity: '晚餐服藥' },
    { day: 'sat', hour: 20, activity: '陪伴看電視' },

    { day: 'sun', hour: 8, activity: '起床盥洗' },
    { day: 'sun', hour: 9, activity: '早餐服藥' },
    { day: 'sun', hour: 10, activity: '家人來訪' },
    { day: 'sun', hour: 12, activity: '午餐' },
    { day: 'sun', hour: 14, activity: '公園散步' },
    { day: 'sun', hour: 16, activity: '點心時間' },
    { day: 'sun', hour: 18, activity: '晚餐服藥' },
    { day: 'sun', hour: 20, activity: '陪伴聊天' },
  ])

  function addEntry(entry: ScheduleEntry) {
    entries.value.push(entry)
  }

  return { entries, addEntry }
})
