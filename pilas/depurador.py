# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

from PySFML import sf
import pilas

class Depurador:
    """Esta clase permite hacer depuraciones visuales.
    
    La depuracion visual en pilas consiste en poder mostrar informacion
    que generalmente es invisible a los jugadores. Por ejemplo, donde
    estan situados los puntos de control, los radios de colision etc.
    
    Esta clase administra varios modos depuracion, que son los
    que dibujan figuras geometricas.
    """
    
    def __init__(self):
        self.modos = []
        self.pizarra = None
    
    def inicia_actualizacion_grafica(self):
        if self.pizarra:
            self.pizarra.limpiar()
            self._mostrar_nombres_de_modos()
        
        for m in self.modos:
            m.inicia_actualizacion_grafica()

    def finaliza_actualizacion_grafica(self):
        for m in self.modos:
            m.finaliza_actualizacion_grafica()
            
    def dibuja_actor(self, actor):
        for m in self.modos:
            m.dibuja_actor(actor)
    
    def pulsa_tecla(self, code):
        if code == sf.Key.F8:
            self._alternar_modo(ModoPuntosDeControl)
        elif code == sf.Key.F9:
            self._alternar_modo(ModoRadiosDeColision)
        elif code == sf.Key.F10:
            self._alternar_modo(ModoArea)
        elif code == sf.Key.F11:
            # pilas.mundo.alternar_fisica()
            pass
        elif code == sf.Key.F12:
            self._alternar_modo(ModoPosicion)

    def _alternar_modo(self, clase_del_modo):
        clases_activas = [x.__class__ for x in self.modos]
        
        if clase_del_modo in clases_activas:
            self._desactivar_modo(clase_del_modo)
        else:
            self._activar_modo(clase_del_modo)
    
    def _activar_modo(self, clase_del_modo):
        if not self.pizarra:
            self.pizarra = pilas.actores.Pizarra()
            
        instancia_del_modo = clase_del_modo(self)
        self.modos.append(instancia_del_modo)
        
    def _desactivar_modo(self, clase_del_modo):
        instancia_a_eliminar = [x for x in self.modos if x.__class__ == clase_del_modo]
        self.modos.remove(instancia_a_eliminar[0])
        
        if not self.modos:
            self.pizarra.eliminar()
            self.pizarra = None

    def _mostrar_nombres_de_modos(self):
        self.pizarra.definir_color(pilas.colores.negro)
        dy = 20
        
        for modo in self.modos:
            self.pizarra.escribir(modo.__class__.__name__ + " habilitado.", 10, dy, tamano=14)
            dy += 20

class ModoDepurador:

    def __init__(self, depurador):
        self.depurador = depurador
        
    def inicia_actualizacion_grafica(self):
        pass
    
    def finaliza_actualizacion_grafica(self):
        pass
     
    def dibuja_actor(self, actor):
        pass
    
    
class ModoPuntosDeControl(ModoDepurador):
    
    def dibuja_actor(self, actor):
        self.depurador.pizarra.pintar_cruz(actor.x, actor.y, 6, pilas.colores.rojo)
        
class ModoRadiosDeColision(ModoDepurador):
    
    def dibuja_actor(self, actor):
        self.depurador.pizarra.definir_color(pilas.colores.verde)
        self.depurador.pizarra.dibujar_circulo(actor.x, actor.y, actor.radio_de_colision, False)
 
 
class ModoArea(ModoDepurador):
    
    def dibuja_actor(self, actor):
        (x, y) = pilas.utils.hacer_coordenada_mundo(actor.izquierda, actor.arriba)
        self.depurador.pizarra.definir_color(pilas.colores.azul)
        self.depurador.pizarra.dibujar_rectangulo(x, y, actor.ancho, actor.alto, False)

class ModoPosicion(ModoDepurador):
    
    def dibuja_actor(self, actor):
        posicion = "(%d, %d)" %(actor.x, actor.y)
        self.depurador.pizarra.definir_color(pilas.colores.violeta)
        (x, y) = pilas.utils.hacer_coordenada_mundo(actor.x, actor.y)
        self.depurador.pizarra.escribir(posicion, x + 20, y + 20, tamano=14)