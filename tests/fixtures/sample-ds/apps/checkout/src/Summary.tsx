import { Card } from '@fixture/ui';
import { CheckoutButton } from './CheckoutButton';
import styles from './Summary.module.css';

export function Summary({ total }: { total: string }) {
  return (
    <Card title="Order summary" className={styles.summary}>
      <p className={styles.total}>Total: {total}</p>
      <CheckoutButton>Place order</CheckoutButton>
    </Card>
  );
}
