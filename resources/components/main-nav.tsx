import { cn } from "@/lib/utils"
import { Link, useLocation } from "react-router-dom"

const navItems = [
  {
    title: "Home",
    href: "/",
  },
  {
    title: "Satellites",
    href: "/satellites",
  },
  {
    title: "Ground Stations",
    href: "/ground-stations",
  },
  {
    title: "Dynamics",
    href: "/dynamics",
  },
  {
    title: "FDS Data",
    href: "/fds-data",
  },
  {
    title: "Orbits",
    href: "/orbits",
  },
  {
    title: "Utils",
    href: "/utils",
  }
]

export function MainNav({
  className,
  ...props
}: React.HTMLAttributes<HTMLElement>) {
  const location = useLocation()

  return (
    <nav
      className={cn("flex items-center space-x-4 lg:space-x-6", className)}
      {...props}
    >
      {navItems.map((item) => (
        <Link
          key={item.href}
          to={item.href}
          className={cn(
            "text-sm font-medium transition-colors hover:text-primary",
            location.pathname === item.href
              ? "text-primary"
              : "text-muted-foreground"
          )}
        >
          {item.title}
        </Link>
      ))}
    </nav>
  )
}
