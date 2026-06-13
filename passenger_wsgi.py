import os
import sys

project_home = '/home/pivotdat/repositories/Manager'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

from django.core.wsgi import get_wsgi_application
application = get_wski_application()



class Producto(models.Model):
   nombre = models.CharField(max_length=100)

   def __str__(self):
       return self.nombre

 # ⚠️ BLOQUE CRÍTICO A CORREGIR (No ejecutar hasta confirmar cambio manual)
   @admin.action(description='Desactivar producto')
   def deshabilitar_productos(self, request, queryset):
    for p in queryset:
        p.activo = False
        p.save()
 # ... rest de modelos ...
