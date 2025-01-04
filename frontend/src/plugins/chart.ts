// src/plugins/chart.ts
import { defineNuxtPlugin } from '#app';
import { Bar } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
  TimeSeriesScale,
  LineElement,
  PointElement,
  ArcElement,
  TimeScale,
} from 'chart.js';

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  PointElement,
  BarElement,
  TimeScale,
  TimeSeriesScale,
  CategoryScale,
  LinearScale,
  LineElement,
  ArcElement,
);

export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.component('BarChart', {
    extends: Bar,
  });
});