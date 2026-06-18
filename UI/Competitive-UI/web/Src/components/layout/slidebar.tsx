import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Brain, 
  FileSearch, 
  Wand2, 
  Eye, 
  Scale, 
  Heart, 
  Sprout,
  Settings 
} from 'lucide-react';
import clsx from 'clsx';

const navigation = [
  { name: 'لوحة التحكم', href: '/', icon: LayoutDashboard },
  { name: 'الحوكمة', href: '/governance', icon: Brain },
  { name: 'التحليل', href: '/analysis', icon: FileSearch },
  { name: 'التوليد', href: '/generation', icon: Wand2 },
  { name: 'الاستشراف', href: '/foresight', icon: Eye },
  { name: 'القانون', href: '/law', icon: Scale },
  { name: 'الطب', href: '/medicine', icon: Heart },
  { name: 'الزراعة', href: '/agriculture', icon: Sprout },
  { name: 'الإعدادات', href: '/settings', icon: Settings },
];

interface SidebarProps {
  isOpen: boolean;
  setIsOpen: (open: boolean) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ isOpen }) => {
  return (
    <aside
      className={clsx(
        'fixed md:relative z-20 w-64 h-full bg-white dark:bg-gray-800 border-l border-gray-200 dark:border-gray-700 transition-transform duration-300',
        isOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'
      )}
    >
      <div className="flex items-center justify-center h-16 border-b border-gray-200 dark:border-gray-700">
        <span className="text-xl font-bold text-blue-600 dark:text-blue-400">🧠 GOE OS</span>
      </div>
      <nav className="p-4 space-y-1">
        {navigation.map((item) => (
          <NavLink
            key={item.name}
            to={item.href}
            className={({ isActive }) =>
              clsx(
                'flex items-center gap-3 px-4 py-2.5 rounded-lg transition-colors',
                isActive
                  ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300'
                  : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
              )
            }
          >
            <item.icon className="w-5 h-5" />
            <span>{item.name}</span>
          </NavLink>
        ))}
      </nav>
    </aside>
  );
};

export default Sidebar;
