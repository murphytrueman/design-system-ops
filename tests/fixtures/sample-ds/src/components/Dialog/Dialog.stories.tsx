import type { Meta, StoryObj } from '@storybook/react';
import { Dialog } from './Dialog';

const meta: Meta<typeof Dialog> = { title: 'Components/Dialog', component: Dialog, tags: ['autodocs'] };
export default meta;

export const Open: StoryObj<typeof Dialog> = {
  args: { isOpen: true, heading: 'Remove item?', children: 'This cannot be undone.', onDismiss: () => {} },
};
