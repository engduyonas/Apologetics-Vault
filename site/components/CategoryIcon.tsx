"use client";

import {
  HelpCircle,
  Crown,
  BookOpen,
  Book,
  Scroll,
  User,
  FileText,
  MessageSquare,
  Globe,
  Users,
  RotateCcw,
  AlignLeft,
  PenTool,
  Wind,
  Heart,
  Landmark,
  Church,
  AlertTriangle,
  MoonStar,
  Flower2,
  Compass,
  Brain,
  Scale,
  RefreshCw,
  Sparkles,
  Cross,
  Star,
} from "lucide-react";

const iconMap: Record<string, React.ComponentType<{ className?: string }>> = {
  "help-circle": HelpCircle,
  crown: Crown,
  "book-open": BookOpen,
  book: Book,
  scroll: Scroll,
  user: User,
  "file-text": FileText,
  "message-square": MessageSquare,
  globe: Globe,
  users: Users,
  "rotate-ccw": RotateCcw,
  "align-left": AlignLeft,
  "pen-tool": PenTool,
  wind: Wind,
  heart: Heart,
  landmark: Landmark,
  church: Church,
  "alert-triangle": AlertTriangle,
  "moon-star": MoonStar,
  flower: Flower2,
  compass: Compass,
  brain: Brain,
  scale: Scale,
  "refresh-cw": RefreshCw,
  sparkles: Sparkles,
  cross: Cross,
  star: Star,
};

export default function CategoryIcon({
  icon,
  className = "w-5 h-5",
}: {
  icon: string;
  className?: string;
}) {
  const Icon = iconMap[icon] || BookOpen;
  return <Icon className={className} />;
}
