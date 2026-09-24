import type { ReactNode } from 'react';
import styles from './Modal.module.css';

export interface ModalProps {
  /** Whether the modal is shown. */
  open: boolean;
  /** Called when the user closes the modal. */
  onClose: () => void;
  /** Heading shown at the top of the modal. */
  title: string;
  children: ReactNode;
}

export function Modal({ open, onClose, title, children }: ModalProps) {
  if (!open) return null;
  return (
    <div className={styles.backdrop}>
      <div className={styles.modal} role="dialog" aria-modal="true" aria-labelledby="modal-title">
        <h2 id="modal-title" className={styles.title}>{title}</h2>
        <div className={styles.body}>{children}</div>
        <button type="button" className={styles.close} onClick={onClose}>Close</button>
      </div>
    </div>
  );
}
