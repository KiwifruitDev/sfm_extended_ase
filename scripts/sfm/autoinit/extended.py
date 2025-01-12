# SFM Extended Animation Set Editor Buttons by KiwifruitDev
# https://github.com/KiwifruitDev/sfm_achievements
# This software is licensed under the MIT License.
# MIT License
# 
# Copyright (c) 2025 KiwifruitDev
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sfm
import sfmApp
from PySide import QtGui, QtCore

class SFMExtended:
    def __init__(self):
        self.app = sfmApp.GetMainWindow()
    def setup(self):
        # Get animation set editor window
        # Using pyside to go through the window hierarchy from the main window
        self.animation_set_editor = self.find_window_by_title(self.app, "QAnimationSetEditor")
        if self.animation_set_editor:
            shouldHide = True # not an exposed option sadly, you can change this to False if you want to keep the original + button
            firstOffset = 41+5
            if shouldHide:
                firstOffset = 2
            sfm.Msg("[EXTENDED ASE] Found the Animation Set Editor!\n")
            # List of all children of the animation set editor
            tabbedbuttonparent = None
            skip = False
            self.actions = []
            # Remove all object names "toolbutton_*" to prevent conflicts
            for child in self.animation_set_editor.findChildren(QtGui.QWidget):
                if child.metaObject().className() == "QToolButton":
                    if child.objectName().startswith("toolbutton_"):
                        child.deleteLater()
            for child in self.animation_set_editor.findChildren(QtGui.QWidget):
                # Get the second QTabbedToolButton
                if(child.metaObject().className() == "CQTabbedToolButton"):
                    if not skip:
                        skip = True
                        continue
                    tabbedbuttonparent = child.parent()
                    # hide child
                    if shouldHide:
                        child.hide()
                    self.actions = child.menu().actions()
                    break
            # Add PySide.QtGui.QToolButton to the toolbuttonparent
            if tabbedbuttonparent:
                # camera
                self.toolbutton_camera = QtGui.QToolButton(tabbedbuttonparent)
                self.toolbutton_camera.setObjectName("toolbutton_camera")
                self.toolbutton_camera.setIconSize(QtCore.QSize(32, 32))
                self.toolbutton_camera.resize(32, 32)
                self.toolbutton_camera.move(firstOffset, 1)
                self.toolbutton_camera.setIcon(QtGui.QIcon("tools:/images/sfm/icon_ase_new_camera.png"))
                self.toolbutton_camera.setToolTip("Create Animation Set for New Camera")
                self.toolbutton_camera.setStatusTip("Create Animation Set for New Camera")
                self.toolbutton_camera.clicked.connect(self.toolbutton_camera_clicked)
                self.toolbutton_camera.pressed.connect(self.toolbutton_camera_pressed)
                self.toolbutton_camera.released.connect(self.toolbutton_camera_released)
                self.toolbutton_camera.show()
                # light
                self.toolbutton_light = QtGui.QToolButton(tabbedbuttonparent)
                self.toolbutton_light.setObjectName("toolbutton_light")
                self.toolbutton_light.setIconSize(QtCore.QSize(32, 32))
                self.toolbutton_light.resize(32, 32)
                self.toolbutton_light.move(firstOffset+32+5, 1)
                self.toolbutton_light.setIcon(QtGui.QIcon("tools:/images/sfm/icon_ase_new_light.png"))
                self.toolbutton_light.setToolTip("Create Animation Set for New Light")
                self.toolbutton_light.setStatusTip("Create Animation Set for New Light")
                self.toolbutton_light.clicked.connect(self.toolbutton_light_clicked)
                self.toolbutton_light.pressed.connect(self.toolbutton_light_pressed)
                self.toolbutton_light.released.connect(self.toolbutton_light_released)
                self.toolbutton_light.show()
                # model
                self.toolbutton_model = QtGui.QToolButton(tabbedbuttonparent)
                self.toolbutton_model.setObjectName("toolbutton_model")
                self.toolbutton_model.setIconSize(QtCore.QSize(32, 32))
                self.toolbutton_model.resize(32, 32)
                self.toolbutton_model.move(firstOffset+32+5+32+5, 1)
                self.toolbutton_model.setIcon(QtGui.QIcon("tools:/images/sfm/icon_ase_new_model.png"))
                self.toolbutton_model.setToolTip("Create Animation Set for New Model")
                self.toolbutton_model.setStatusTip("Create Animation Set for New Model")
                self.toolbutton_model.clicked.connect(self.toolbutton_model_clicked)
                self.toolbutton_model.pressed.connect(self.toolbutton_model_pressed)
                self.toolbutton_model.released.connect(self.toolbutton_model_released)
                self.toolbutton_model.show()
                # particle
                self.toolbutton_particle = QtGui.QToolButton(tabbedbuttonparent)
                self.toolbutton_particle.setObjectName("toolbutton_particle")
                self.toolbutton_particle.setIconSize(QtCore.QSize(32, 32))
                self.toolbutton_particle.resize(32, 32)
                self.toolbutton_particle.move(firstOffset+32+5+32+5+32+5, 1)
                self.toolbutton_particle.setIcon(QtGui.QIcon("tools:/images/sfm/icon_ase_new_particles.png"))
                self.toolbutton_particle.setToolTip("Create Animation Set for New Particle System")
                self.toolbutton_particle.setStatusTip("Create Animation Set for New Particle System")
                self.toolbutton_particle.clicked.connect(self.toolbutton_particle_clicked)
                self.toolbutton_particle.pressed.connect(self.toolbutton_particle_pressed)
                self.toolbutton_particle.released.connect(self.toolbutton_particle_released)
                self.toolbutton_particle.show()
                # pick element
                self.toolbutton_pick_element = QtGui.QToolButton(tabbedbuttonparent)
                self.toolbutton_pick_element.setObjectName("toolbutton_pick_element")
                self.toolbutton_pick_element.setIconSize(QtCore.QSize(40, 32))
                self.toolbutton_pick_element.resize(40, 32)
                self.toolbutton_pick_element.move(firstOffset+32+5+32+5+32+5+32+5, 1)
                self.toolbutton_pick_element.setIcon(QtGui.QIcon("tools:/images/sfm/icon_ase_pick_element.png"))
                self.toolbutton_pick_element.setToolTip("Create Animation Set(s) for Existing Element(s)")
                self.toolbutton_pick_element.setStatusTip("Create Animation Set(s) for Existing Element(s)")
                self.toolbutton_pick_element.clicked.connect(self.toolbutton_pick_element_clicked)
                self.toolbutton_pick_element.pressed.connect(self.toolbutton_pick_element_pressed)
                self.toolbutton_pick_element.released.connect(self.toolbutton_pick_element_released)
                self.toolbutton_pick_element.show()
                # create preset
                self.toolbutton_create_preset = QtGui.QToolButton(tabbedbuttonparent)
                self.toolbutton_create_preset.setObjectName("toolbutton_create_preset")
                self.toolbutton_create_preset.setIconSize(QtCore.QSize(32, 32))
                self.toolbutton_create_preset.resize(32, 32)
                self.toolbutton_create_preset.move(firstOffset+32+5+32+5+32+5+32+5+40+5, 1)
                self.toolbutton_create_preset.setIcon(QtGui.QIcon("tools:/images/sfm/icon_ase_new_element.png"))
                self.toolbutton_create_preset.setToolTip("Create Preset")
                self.toolbutton_create_preset.setStatusTip("Create Preset")
                self.toolbutton_create_preset.clicked.connect(self.toolbutton_create_preset_clicked)
                self.toolbutton_create_preset.pressed.connect(self.toolbutton_create_preset_pressed)
                self.toolbutton_create_preset.released.connect(self.toolbutton_create_preset_released)
                self.toolbutton_create_preset.show()
                sfm.Msg("[EXTENDED ASE] ToolButtons added!\n")
            else:
                sfm.Msg("[EXTENDED ASE] ToolButton parent not found.\n")
        else:
            sfm.Msg("[EXTENDED ASE] Animation Set Editor window not found.\n")
    def find_window_by_title(self, parent, title):
        for child in parent.findChildren(QtGui.QWidget):
            # windowTitle doesn't work sadly, using a diff method
            if child.objectName() == title:
                return child
            result = self.find_window_by_title(child, title)
            if result:
                return result
        return None
    def toolbutton_camera_clicked(self):
        self.actions[0].trigger()
    def toolbutton_camera_pressed(self):
        self.toolbutton_camera.setIcon(QtGui.QIcon("tools:/images/sfm/icon_ase_new_camera_activated.png"))
    def toolbutton_camera_released(self):
        self.toolbutton_camera.setIcon(QtGui.QIcon("tools:/images/sfm/icon_ase_new_camera.png"))
    def toolbutton_light_clicked(self):
        self.actions[1].trigger()
    def toolbutton_light_pressed(self):
        self.toolbutton_light.setIcon(QtGui.QIcon("tools:/images/sfm/icon_ase_new_light_activated.png"))
    def toolbutton_light_released(self):
        self.toolbutton_light.setIcon(QtGui.QIcon("tools:/images/sfm/icon_ase_new_light.png"))
    def toolbutton_model_clicked(self):
        self.actions[2].trigger()
    def toolbutton_model_pressed(self):
        self.toolbutton_model.setIcon(QtGui.QIcon("tools:/images/sfm/icon_ase_new_model_activated.png"))
    def toolbutton_model_released(self):
        self.toolbutton_model.setIcon(QtGui.QIcon("tools:/images/sfm/icon_ase_new_model.png"))
    def toolbutton_particle_clicked(self):
        self.actions[3].trigger()
    def toolbutton_particle_pressed(self):
        self.toolbutton_particle.setIcon(QtGui.QIcon("tools:/images/sfm/icon_ase_new_particles_activated.png"))
    def toolbutton_particle_released(self):
        self.toolbutton_particle.setIcon(QtGui.QIcon("tools:/images/sfm/icon_ase_new_particles.png"))
    def toolbutton_pick_element_clicked(self):
        self.actions[4].trigger()
    def toolbutton_pick_element_pressed(self):
        self.toolbutton_pick_element.setIcon(QtGui.QIcon("tools:/images/sfm/icon_ase_pick_element_activated.png"))
    def toolbutton_pick_element_released(self):
        self.toolbutton_pick_element.setIcon(QtGui.QIcon("tools:/images/sfm/icon_ase_pick_element.png"))
    def toolbutton_create_preset_clicked(self):
        self.actions[6].trigger()
    def toolbutton_create_preset_pressed(self):
        self.toolbutton_create_preset.setIcon(QtGui.QIcon("tools:/images/sfm/icon_ase_new_element_activated.png"))
    def toolbutton_create_preset_released(self):
        self.toolbutton_create_preset.setIcon(QtGui.QIcon("tools:/images/sfm/icon_ase_new_element.png"))

if __name__ == "__main__":
    extendedExists = globals().get("global_sfmExtended")
    # delete existing instance
    if extendedExists:
        del extendedExists
    sfmExtended = SFMExtended()
    sfmExtended.setup()
    globals()["global_sfmExtended"] = sfmExtended
