---
description: read this file to understand how to fetch data in the project.
---

# Data Fetching Guidelines

Thsi document outlines the best practices and guidelines for fetching data in our Next.js application. Adhering to this guidelines will ensure consistency, performance, and maintainability across the codebase.

## 1. Use Server Components for Data Fetching

In Next.js, ALWAYS use Server Components for data fetching. NEVER use Client Components for data fetching.

## 2. Data Fetching Methods

ALWAYS use teh helper functions in the /data directory to fetch data. Never fetch data directly in the components.

ALL helper functions in the /data directory should use Drizzle ORM for database interactions.
