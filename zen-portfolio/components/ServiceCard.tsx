import Image from 'next/image';
import Link from 'next/link';
import { motion } from 'framer-motion';

export interface ServiceCardProps {
  title: string;
  description: string;
  imageSrc: string; // path relative to /public
  link?: string;
}

export function ServiceCard({ title, description, imageSrc, link }: ServiceCardProps) {
  const CardContent = (
    <motion.div
      className="glass-card rounded-2xl overflow-hidden shadow-lg hover:shadow-2xl transition-shadow duration-300"
      whileHover={{ scale: 1.02 }}
    >
      <div className="relative h-48 w-full">
        <Image
          src={imageSrc}
          alt={title}
          fill
          className="object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent" />
      </div>
      <div className="p-4">
        <h3 className="text-xl font-mono font-bold text-foreground mb-2">{title}</h3>
        <p className="text-muted-foreground font-mono text-sm leading-relaxed">
          {description}
        </p>
      </div>
    </motion.div>
  );

  return link ? (
    <Link href={link} className="block">
      {CardContent}
    </Link>
  ) : (
    CardContent
  );
}
