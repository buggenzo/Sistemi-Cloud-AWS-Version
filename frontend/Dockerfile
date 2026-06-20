FROM nginx:alpine

# Rimuovi la configurazione di default di Nginx
RUN rm /etc/nginx/conf.d/default.conf

# Copia la tua configurazione personalizzata
COPY nginx.conf /etc/nginx/conf.d/

# Copia il tuo file HTML
COPY index.html /usr/share/nginx/html/

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]