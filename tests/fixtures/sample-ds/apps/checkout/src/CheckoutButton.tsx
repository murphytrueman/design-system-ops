import type { ButtonHTMLAttributes } from 'react';
import styles from './CheckoutButton.module.css';

export function CheckoutButton({ className, ...props }: ButtonHTMLAttributes<HTMLButtonElement>) {
  return <button className={[styles.button, className].filter(Boolean).join(' ')} {...props} />;
}
