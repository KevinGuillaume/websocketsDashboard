import { usePriceSocket } from '../hooks/usePriceSocket';
import styles from './PriceDashboard.module.css';

export default function PriceDashboard() {
  const { prices, status } = usePriceSocket();
  const entries = Object.entries(prices);

  return (
    <div className={styles.dashboard}>
      <div className={styles.header}>
        <h2 className={styles.title}>Market Prices</h2>
        <div className={styles.statusBadge}>
          <span className={`${styles.dot} ${styles[status]}`} />
          {status}
        </div>
      </div>

      {entries.length === 0 ? (
        <p className={styles.empty}>Waiting for price data…</p>
      ) : (
        <div className={styles.grid}>
          {entries.map(([symbol, price]) => (
            <div key={symbol} className={styles.card}>
              <span className={styles.symbol}>{symbol}</span>
              <span className={styles.price}>${parseFloat(price as string).toFixed(2)}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}