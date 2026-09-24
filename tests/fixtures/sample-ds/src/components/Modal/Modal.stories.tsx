import type { Meta, StoryObj } from '@storybook/react';
import { Modal } from './Modal';

const meta: Meta<typeof Modal> = { title: 'Components/Modal', component: Modal, tags: ['autodocs'] };
export default meta;

export const Open: StoryObj<typeof Modal> = {
  args: { open: true, title: 'Discard changes?', children: 'You have unsaved edits.', onClose: () => {} },
};
