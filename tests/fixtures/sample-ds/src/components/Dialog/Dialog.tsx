import type { ReactNode } from 'react';
import styles from './Dialog.module.css';

export interface DialogProps {
  /** Whether the dialog is shown. */
  isOpen: boolean;
  /** Called when the user dismisses the dialog. */
  onDismiss: () => void;
  /** Heading shown at the top of the dialog. */
  heading: string;
  children: ReactNode;
}

export function Dialog({ isOpen, onDismiss, heading, children }: DialogProps) {
  return (
    <dialog className={styles.dialog} open={isOpen} aria-labelledby="dialog-heading">
      <h2 id="dialog-heading" className={styles.heading}>{heading}</h2>
      <div className={styles.body}>{children}</div>
      <button type="button" className={styles.dismiss} onClick={onDismiss}>Dismiss</button>
    </dialog>
  );
}
