# -*- coding: utf-8 -*-
import os
import sys

from PyQt4 import QtCore, QtGui

import pilasengine
from pilasengine.interprete.interprete_base import Ui_InterpreteWindow


class VentanaInterprete(Ui_InterpreteWindow):

    def setupUi(self, main):
        self.main = main
        Ui_InterpreteWindow.setupUi(self, main)
        self.iniciar_interfaz()

    def iniciar_interfaz(self):
        self.scope = self._insertar_ventana_principal_de_pilas()
        self._insertar_consola_interactiva(self.scope)

        # Haciendo que el panel de pilas y el interprete no se puedan
        # ocultar completamente.
        self.splitter_vertical.setCollapsible(1, False)
        self.splitter.setCollapsible(0, False)

        # Define el tamaño inicial de la consola.
        self.splitter.setSizes([300, 100])

        self.colapsar_ayuda()
        self.cargar_ayuda()
        self.navegador.history().setMaximumItemCount(0)

        self._conectar_botones()
        self._conectar_observadores_splitters()

    def _conectar_botones(self):
        # Botón del manual
        self.definir_icono(self.manual_button, 'iconos/manual.png')
        self.manual_button.connect(self.manual_button, QtCore.SIGNAL("clicked()"), self.cuando_pulsa_el_boton_manual)

        # Botón del interprete
        self.definir_icono(self.interprete_button, 'iconos/interprete.png')
        self.interprete_button.connect(self.interprete_button, QtCore.SIGNAL("clicked()"), self.cuando_pulsa_el_boton_interprete)

        # Botón del guardar
        self.definir_icono(self.guardar_button, 'iconos/guardar.png')
        self.interprete_button.connect(self.guardar_button, QtCore.SIGNAL("clicked()"), self.cuando_pulsa_el_boton_guardar)

        # F7 Modo informacion de sistema
        self.definir_icono(self.pushButton_6, 'iconos/f07.png')
        self.pushButton_6.connect(self.pushButton_6, QtCore.SIGNAL("clicked()"), self.pulsa_boton_depuracion)

        # F8 Modo puntos de control
        self.definir_icono(self.pushButton_5, 'iconos/f08.png')
        self.pushButton_5.connect(self.pushButton_5, QtCore.SIGNAL("clicked()"), self.pulsa_boton_depuracion)

        # F9 Modo radios de colision
        self.definir_icono(self.pushButton_4, 'iconos/f09.png')
        self.pushButton_4.connect(self.pushButton_4, QtCore.SIGNAL("clicked()"), self.pulsa_boton_depuracion)

        # F10 Modo areas de colision
        self.definir_icono(self.pushButton_3, 'iconos/f10.png')
        self.pushButton_3.connect(self.pushButton_3, QtCore.SIGNAL("clicked()"), self.pulsa_boton_depuracion)

        # F11 Modo fisica
        self.definir_icono(self.pushButton_2, 'iconos/f11.png')
        self.pushButton_2.connect(self.pushButton_2, QtCore.SIGNAL("clicked()"), self.pulsa_boton_depuracion)

        # F12 Modo depuracion de posicion
        self.definir_icono(self.pushButton, 'iconos/f12.png')
        self.pushButton.connect(self.pushButton, QtCore.SIGNAL("clicked()"), self.pulsa_boton_depuracion)

    def _conectar_observadores_splitters(self):
        # Observa los deslizadores para mostrar mostrar los botones de ayuda o consola activados.
        self.splitter_vertical.connect(self.splitter_vertical, QtCore.SIGNAL("splitterMoved(int, int)"), self.cuando_mueve_deslizador_vertical)
        self.splitter.connect(self.splitter, QtCore.SIGNAL("splitterMoved(int, int)"), self.cuando_mueve_deslizador)

    def colapsar_ayuda(self):
        self.splitter_vertical.setSizes([0])
        self.manual_button.setChecked(False)

    def cargar_ayuda(self):
        file_path = pilasengine.utils.obtener_ruta_al_recurso('manual/index.html')
        file_path = os.path.abspath(file_path)
        base_dir =  QtCore.QUrl.fromLocalFile(file_path)
        self.navegador.load(base_dir)

    def definir_icono(self, boton, ruta):
        icon = QtGui.QIcon()
        archivo = pilasengine.utils.obtener_ruta_al_recurso(ruta)
        icon.addFile(archivo, QtCore.QSize(), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        boton.setIcon(icon)
        boton.setText('')

    def cuando_mueve_deslizador_vertical(self, a1, a2):
        self.manual_button.setChecked(a1 != 0)

    def cuando_mueve_deslizador(self, a1, a2):
        altura_interprete = self.splitter.sizes()[1]
        self.interprete_button.setChecked(altura_interprete != 0)

    def cuando_pulsa_el_boton_manual(self):
        if self.manual_button.isChecked():
            self.splitter_vertical.setSizes([300])
        else:
            self.splitter_vertical.setSizes([0])

    def cuando_pulsa_el_boton_interprete(self):
        if self.interprete_button.isChecked():
            self.splitter.setSizes([300, 100])
        else:
            self.splitter.setSizes([300, 0])

    def pulsa_boton_depuracion(self):
        pilas = self.scope['pilas']
        pilas.depurador.definir_modos(
                            info=self.pushButton_6.isChecked(),              # F07
                            puntos_de_control=self.pushButton_5.isChecked(), # F08
                            radios=self.pushButton_4.isChecked(),            # F09
                            areas=self.pushButton_3.isChecked(),             # F10
                            fisica=self.pushButton_2.isChecked(),            # F11
                            posiciones=self.pushButton.isChecked(),          # F12
                )

    def raw_input(self, mensaje):
        text, _ = QtGui.QInputDialog.getText(self.main, "raw_input", mensaje)
        return str(text)

    def input(self, mensaje):
        text, _ = QtGui.QInputDialog.getText(self.main, "raw_input", mensaje)
        return eval(str(text))

    def help(self, objeto=None):
        if objeto:
            print help(objeto)
        else:
            print "Escribe help(objeto) para obtener ayuda sobre ese objeto."

    def _insertar_ventana_principal_de_pilas(self):
        pilas = pilasengine.iniciar(640, 400)
        aceituna = pilas.actores.Aceituna()
        scope = {'pilas': pilas, 'aceituna': aceituna, 'self': self}
        ventana = pilas.obtener_widget()

        ventana.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.canvas.setFocus()
        self.canvas.addWidget(ventana)
        self.canvas.setCurrentWidget(ventana)
        return scope

    def _insertar_consola_interactiva(self, scope):
        codigo_inicial = [
                'import pilasengine',
                '',
                'pilas = pilasengine.iniciar()',
                'aceituna = pilas.actores.Aceituna()',
        ]

        pilasengine.utils.verificar_si_lanas_existe(self.main)

        import sys
        sys.path.append('../lanas')
        import lanas

        consola = lanas.interprete.Ventana(self.splitter, scope, "\n".join(codigo_inicial))
        self.console.addWidget(consola)
        self.console.setCurrentWidget(consola)
        self.consola = consola
        self.consola.text_edit.setFocus()

    def cuando_pulsa_el_boton_guardar(self):
        self.consola.text_edit.guardar_contenido_con_dialogo()


def abrir():
    MainWindow = QtGui.QMainWindow()

    ui = VentanaInterprete()
    ui.setupUi(MainWindow)

    MainWindow.show()
    MainWindow.raise_()

    return MainWindow