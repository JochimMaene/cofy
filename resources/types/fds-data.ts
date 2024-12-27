export interface FdsData {
    id: number;
    name: string;
    URL: string;
    cron: string;
    lastUpdate: string;
    nextUpdate: string;
    status: 'updated' | 'out_of_date';
}