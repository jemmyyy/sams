import { defineStore } from 'pinia';
import api from '../api';

export interface Transaction {
  id: string;
  player_name: string;
  amount: number;
  type: 'Payment' | 'Refund' | 'Credit';
  status: 'Completed' | 'Pending' | 'Failed';
  date: string;
}

export const useFinancesStore = defineStore('finances', {
  state: () => ({
    transactions: [] as Transaction[],
    revenue_mtd: 0,
    loading: false
  }),
  actions: {
    async fetchTransactions() {
      this.loading = true;
      try {
        const response = await api.get('payments/');
        this.transactions = response.data.results || response.data;
        // Mocking revenue for demo if backend doesn't provide it
        this.revenue_mtd = this.transactions.reduce((acc, t) => acc + (t.status === 'Completed' ? t.amount : 0), 0);
      } catch (err) {
        console.error('Failed to fetch transactions');
      } finally {
        this.loading = false;
      }
    }
  }
});
