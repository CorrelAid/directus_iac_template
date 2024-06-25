FROM directus/directus:12.0.0

USER root
RUN corepack enable
USER node

RUN pnpm install directus-extension-schema-sync an

COPY ./email-templates ./templates
