import type { Meta, StoryObj } from '@storybook/react';
import { Card } from './Card';

const meta: Meta<typeof Card> = { title: 'Components/Card', component: Card, tags: ['autodocs'] };
export default meta;

export const Default: StoryObj<typeof Card> = { args: { title: 'Billing', children: 'Your plan renews on 1 October.' } };
