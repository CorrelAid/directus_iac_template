FROM directus/directus:10.12.1

USER root
RUN corepack enable
USER node

RUN pnpm install directus-extension-schema-sync an

COPY ./email-templates ./templates
