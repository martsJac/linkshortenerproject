CREATE TABLE "links" (
	"id" serial PRIMARY KEY NOT NULL,
	"user_id" text NOT NULL,
	"original_url" text NOT NULL,
	"short_code" varchar(20) NOT NULL,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	"updated_at" timestamp with time zone DEFAULT now() NOT NULL,
	CONSTRAINT "links_short_code_unique" UNIQUE("short_code")
);
