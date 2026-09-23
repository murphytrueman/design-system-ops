import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

const meta: Meta<typeof Button> = { title: 'Components/Button', component: Button, tags: ['autodocs'] };
export default meta;

export const Primary: StoryObj<typeof Button> = { args: { children: 'Save changes' } };
export const Secondary: StoryObj<typeof Button> = { args: { variant: 'secondary', children: 'Cancel' } };
