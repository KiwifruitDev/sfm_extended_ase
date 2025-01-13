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
import json
from PySide import QtGui, QtCore

class ToolsButtonEventFilter(QtCore.QObject):
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Resize:
            sfmExtended = globals().get("global_sfmExtended")
            if sfmExtended:
                tools_button = sfmExtended.toolbutton_tools
                tools_button.move(obj.width()-tools_button.width()-2, tools_button.y())
        return False

class SFMExtended:
    def __init__(self):
        self.version = "1.3"
        self.app = sfmApp.GetMainWindow()
        self.plus_button = None
        self.toolbutton_camera = None
        self.toolbutton_light = None
        self.toolbutton_model = None
        self.toolbutton_particle = None
        self.toolbutton_pick_element = None
        self.toolbutton_create_preset = None
        self.separator_offset = 5
        self.small_width = 32
        self.large_width = 40
        self.height = 32
        self.x_offset = 1
        self.y_offset = 1
        self.tools_menu_shown = False
        self.found_event_filter = ToolsButtonEventFilter()
        self.setup_settings()
        self.setup()
        self.apply_settings()
    def setup_settings(self):
        self.savedata = "extended_options.json"
        self.default_settings = {
            "show_plus_button": True,
            "shown_buttons": {
                "camera": True,
                "light": True,
                "model": True,
                "particle": True,
                "pick_element": True,
                "create_preset": True
            }
        }
        self.settings = self.default_settings
        self.load_settings()
    def load_settings(self):
        # Load settings from json
        try:
            with open(self.savedata, "r") as f:
                self.settings = json.load(f)
        except:
            # Create new settings file
            sfm.Msg("[EXTENDED ASE] Settings file not found, creating new settings file.\n")
            self.settings = self.default_settings
            self.save_settings()
    def save_settings(self):
        # Save settings to json
        with open(self.savedata, "w") as f:
            json.dump(self.settings, f)
    def apply_settings(self):
        x_offset = self.x_offset
        if self.plus_button:
            if self.settings["show_plus_button"]:
                self.plus_button.show()
                x_offset += self.large_width+self.separator_offset
            else:
                self.plus_button.hide()
                x_offset += 1
        if self.toolbutton_camera:
            if self.settings["shown_buttons"]["camera"]:
                self.toolbutton_camera.move(x_offset, self.y_offset)
                self.toolbutton_camera.show()
                x_offset += self.small_width+self.separator_offset
            else:
                self.toolbutton_camera.hide()
        if self.toolbutton_light:
            if self.settings["shown_buttons"]["light"]:
                self.toolbutton_light.move(x_offset, self.y_offset)
                self.toolbutton_light.show()
                x_offset += self.small_width+self.separator_offset
            else:
                self.toolbutton_light.hide()
        if self.toolbutton_model:
            if self.settings["shown_buttons"]["model"]:
                self.toolbutton_model.move(x_offset, self.y_offset)
                self.toolbutton_model.show()
                x_offset += self.small_width+self.separator_offset
            else:
                self.toolbutton_model.hide()
        if self.toolbutton_particle:
            if self.settings["shown_buttons"]["particle"]:
                self.toolbutton_particle.move(x_offset, self.y_offset)
                self.toolbutton_particle.show()
                x_offset += self.small_width+self.separator_offset
            else:
                self.toolbutton_particle.hide()
        if self.toolbutton_pick_element:
            if self.settings["shown_buttons"]["pick_element"]:
                self.toolbutton_pick_element.move(x_offset, self.y_offset)
                self.toolbutton_pick_element.show()
                x_offset += self.large_width+self.separator_offset
            else:
                self.toolbutton_pick_element.hide()
        if self.toolbutton_create_preset:
            if self.settings["shown_buttons"]["create_preset"]:
                self.toolbutton_create_preset.move(x_offset, self.y_offset)
                self.toolbutton_create_preset.show()
            else:
                self.toolbutton_create_preset.hide()
    def setup(self):
        # Get animation set editor window
        # Using pyside to go through the window hierarchy from the main window
        self.animation_set_editor = self.find_window_by_title(self.app, "QAnimationSetEditor")
        if self.animation_set_editor:
            sfm.Msg("[EXTENDED ASE] Found the Animation Set Editor!\n")
            # List of all children of the animation set editor
            tabbedbuttonparent = None
            self.actions = []
            # Remove all object names "toolbutton_*" to prevent conflicts
            for child in self.animation_set_editor.findChildren(QtGui.QWidget):
                if child.metaObject().className() == "QToolButton":
                    if child.objectName().startswith("toolbutton_"):
                        child.deleteLater()
            addedSetting = False
            for child in self.animation_set_editor.findChildren(QtGui.QWidget):
                # Get the second QTabbedToolButton
                if(child.metaObject().className() == "CQTabbedToolButton"):
                    # The first QTabbedToolButton is the settings menu
                    if not addedSetting:
                        addedSetting = True
                        sfm.Msg("[EXTENDED ASE] Found the settings menu!\n")
                        self.tools_button = child
                        self.tools_button.menu().aboutToShow.connect(self.toolbutton_tools_pressed)
                        self.tools_button.menu().aboutToHide.connect(self.toolbutton_tools_released)
                        self.tools_button.hide()
                        continue
                    # The second QTabbedToolButton is the + menu
                    tabbedbuttonparent = child.parent()
                    self.actions = child.menu().actions()
                    self.plus_button = child
                    break
            # Add PySide.QtGui.QToolButton to the toolbuttonparent
            if tabbedbuttonparent:
                # where to place the buttons
                x_offset = self.x_offset+self.large_width+self.separator_offset
                # camera
                self.toolbutton_camera = QtGui.QToolButton(tabbedbuttonparent)
                self.toolbutton_camera.setObjectName("toolbutton_camera")
                self.toolbutton_camera.setIconSize(QtCore.QSize(self.small_width, self.height))
                self.toolbutton_camera.resize(self.small_width, self.height)
                self.toolbutton_camera.move(x_offset, self.y_offset)
                self.toolbutton_camera.setIcon(QtGui.QIcon("tools:/images/sfm/icon_ase_new_camera.png"))
                self.toolbutton_camera.setToolTip("Create Animation Set for New Camera")
                self.toolbutton_camera.clicked.connect(self.toolbutton_camera_clicked)
                self.toolbutton_camera.pressed.connect(self.toolbutton_camera_pressed)
                self.toolbutton_camera.released.connect(self.toolbutton_camera_released)
                self.toolbutton_camera.show()
                x_offset += self.small_width+self.separator_offset
                # light
                self.toolbutton_light = QtGui.QToolButton(tabbedbuttonparent)
                self.toolbutton_light.setObjectName("toolbutton_light")
                self.toolbutton_light.setIconSize(QtCore.QSize(self.small_width, self.height))
                self.toolbutton_light.resize(self.small_width, self.height)
                self.toolbutton_light.move(x_offset, self.y_offset)
                self.toolbutton_light.setIcon(QtGui.QIcon("tools:/images/sfm/icon_ase_new_light.png"))
                self.toolbutton_light.setToolTip("Create Animation Set for New Light")
                self.toolbutton_light.clicked.connect(self.toolbutton_light_clicked)
                self.toolbutton_light.pressed.connect(self.toolbutton_light_pressed)
                self.toolbutton_light.released.connect(self.toolbutton_light_released)
                self.toolbutton_light.show()
                x_offset += self.small_width+self.separator_offset
                # model
                self.toolbutton_model = QtGui.QToolButton(tabbedbuttonparent)
                self.toolbutton_model.setObjectName("toolbutton_model")
                self.toolbutton_model.setIconSize(QtCore.QSize(self.small_width, self.height))
                self.toolbutton_model.resize(self.small_width, self.height)
                self.toolbutton_model.move(x_offset, self.y_offset)
                self.toolbutton_model.setIcon(QtGui.QIcon("tools:/images/sfm/icon_ase_new_model.png"))
                self.toolbutton_model.setToolTip("Create Animation Set for New Model")
                self.toolbutton_model.clicked.connect(self.toolbutton_model_clicked)
                self.toolbutton_model.pressed.connect(self.toolbutton_model_pressed)
                self.toolbutton_model.released.connect(self.toolbutton_model_released)
                self.toolbutton_model.show()
                x_offset += self.small_width+self.separator_offset
                # particle
                self.toolbutton_particle = QtGui.QToolButton(tabbedbuttonparent)
                self.toolbutton_particle.setObjectName("toolbutton_particle")
                self.toolbutton_particle.setIconSize(QtCore.QSize(self.small_width, self.height))
                self.toolbutton_particle.resize(self.small_width, self.height)
                self.toolbutton_particle.move(x_offset, self.y_offset)
                self.toolbutton_particle.setIcon(QtGui.QIcon("tools:/images/sfm/icon_ase_new_particles.png"))
                self.toolbutton_particle.setToolTip("Create Animation Set for New Particle System")
                self.toolbutton_particle.clicked.connect(self.toolbutton_particle_clicked)
                self.toolbutton_particle.pressed.connect(self.toolbutton_particle_pressed)
                self.toolbutton_particle.released.connect(self.toolbutton_particle_released)
                self.toolbutton_particle.show()
                x_offset += self.small_width+self.separator_offset
                # pick element
                self.toolbutton_pick_element = QtGui.QToolButton(tabbedbuttonparent)
                self.toolbutton_pick_element.setObjectName("toolbutton_pick_element")
                self.toolbutton_pick_element.setIconSize(QtCore.QSize(self.large_width, self.height))
                self.toolbutton_pick_element.resize(self.large_width, self.height)
                self.toolbutton_pick_element.move(x_offset, self.y_offset)
                self.toolbutton_pick_element.setIcon(QtGui.QIcon("tools:/images/sfm/icon_ase_pick_element.png"))
                self.toolbutton_pick_element.setToolTip("Create Animation Set(s) for Existing Element(s)")
                self.toolbutton_pick_element.clicked.connect(self.toolbutton_pick_element_clicked)
                self.toolbutton_pick_element.pressed.connect(self.toolbutton_pick_element_pressed)
                self.toolbutton_pick_element.released.connect(self.toolbutton_pick_element_released)
                self.toolbutton_pick_element.show()
                x_offset += self.large_width+self.separator_offset
                # create preset
                self.toolbutton_create_preset = QtGui.QToolButton(tabbedbuttonparent)
                self.toolbutton_create_preset.setObjectName("toolbutton_create_preset")
                self.toolbutton_create_preset.setIconSize(QtCore.QSize(self.small_width, self.height))
                self.toolbutton_create_preset.resize(self.small_width, self.height)
                self.toolbutton_create_preset.move(x_offset, self.y_offset)
                self.toolbutton_create_preset.setIcon(QtGui.QIcon("tools:/images/sfm/icon_ase_new_element.png"))
                self.toolbutton_create_preset.setToolTip("Create Preset")
                self.toolbutton_create_preset.clicked.connect(self.toolbutton_create_preset_clicked)
                self.toolbutton_create_preset.pressed.connect(self.toolbutton_create_preset_pressed)
                self.toolbutton_create_preset.released.connect(self.toolbutton_create_preset_released)
                self.toolbutton_create_preset.show()
                # tools (right aligned, where self.tools_button is)
                self.toolbutton_tools = QtGui.QToolButton(tabbedbuttonparent)
                self.toolbutton_tools.setObjectName("toolbutton_tools")
                self.toolbutton_tools.setIconSize(QtCore.QSize(self.large_width, self.height))
                self.toolbutton_tools.resize(self.large_width, self.height)
                self.toolbutton_tools.move(self.animation_set_editor.width()-self.large_width-2, self.y_offset)
                self.toolbutton_tools.setIcon(QtGui.QIcon("tools:/images/sfm/icon_gear.png"))
                self.toolbutton_tools.setToolTip("Tools")
                self.toolbutton_tools.pressed.connect(self.toolbutton_tools_clicked)
                # update event override (used to position)
                self.animation_set_editor.installEventFilter(self.found_event_filter)
                self.toolbutton_tools.show()
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
    def toolbutton_tools_clicked(self):
        if not self.tools_menu_shown:
            self.tools_button.menu().exec_(self.toolbutton_tools.mapToGlobal(QtCore.QPoint(0, self.toolbutton_tools.height())))
    def toolbutton_tools_pressed(self):
        self.toolbutton_tools.setIcon(QtGui.QIcon("tools:/images/sfm/icon_gear_activated.png"))
        self.tools_menu_shown = True
        menu = self.tools_button.menu()
        # Add separator
        self.separator = QtGui.QAction(menu)
        self.separator.setSeparator(True)
        menu.addAction(self.separator)
        # Add "Show + (Add) Button" action
        self.show_plus_button = QtGui.QAction(menu)
        self.show_plus_button.setText("Show + (Add) Button")
        self.show_plus_button.setCheckable(True)
        self.show_plus_button.setChecked(self.settings["show_plus_button"])
        self.show_plus_button.triggered.connect(self.show_plus_button_toggled)
        menu.addAction(self.show_plus_button)
        # Add "Show Camera Button" action
        self.show_camera_button = QtGui.QAction(menu)
        self.show_camera_button.setText("Show Camera Button")
        self.show_camera_button.setCheckable(True)
        self.show_camera_button.setChecked(self.settings["shown_buttons"]["camera"])
        self.show_camera_button.triggered.connect(self.show_camera_button_toggled)
        menu.addAction(self.show_camera_button)
        # Add "Show Light Button" action
        self.show_light_button = QtGui.QAction(menu)
        self.show_light_button.setText("Show Light Button")
        self.show_light_button.setCheckable(True)
        self.show_light_button.setChecked(self.settings["shown_buttons"]["light"])
        self.show_light_button.triggered.connect(self.show_light_button_toggled)
        menu.addAction(self.show_light_button)
        # Add "Show Model Button" action
        self.show_model_button = QtGui.QAction(menu)
        self.show_model_button.setText("Show Model Button")
        self.show_model_button.setCheckable(True)
        self.show_model_button.setChecked(self.settings["shown_buttons"]["model"])
        self.show_model_button.triggered.connect(self.show_model_button_toggled)
        menu.addAction(self.show_model_button)
        # Add "Show Particle System Button" action
        self.show_particle_button = QtGui.QAction(menu)
        self.show_particle_button.setText("Show Particle System Button")
        self.show_particle_button.setCheckable(True)
        self.show_particle_button.setChecked(self.settings["shown_buttons"]["particle"])
        self.show_particle_button.triggered.connect(self.show_particle_button_toggled)
        menu.addAction(self.show_particle_button)
        # Add "Show Existing Element(s) Button" action
        self.show_pick_element_button = QtGui.QAction(menu)
        self.show_pick_element_button.setText("Show Existing Element(s) Button")
        self.show_pick_element_button.setCheckable(True)
        self.show_pick_element_button.setChecked(self.settings["shown_buttons"]["pick_element"])
        self.show_pick_element_button.triggered.connect(self.show_pick_element_button_toggled)
        menu.addAction(self.show_pick_element_button)
        # Add "Show Preset Button" action
        self.show_create_preset_button = QtGui.QAction(menu)
        self.show_create_preset_button.setText("Show Preset Button")
        self.show_create_preset_button.setCheckable(True)
        self.show_create_preset_button.setChecked(self.settings["shown_buttons"]["create_preset"])
        self.show_create_preset_button.triggered.connect(self.show_create_preset_button_toggled)
        menu.addAction(self.show_create_preset_button)
        # Add header
        self.header = QtGui.QAction(menu)
        self.header.setText("Extended ASE v"+self.version+" by KiwifruitDev")
        self.header.setEnabled(False)
        menu.addAction(self.header)
    def toolbutton_tools_released(self):
        self.toolbutton_tools.setIcon(QtGui.QIcon("tools:/images/sfm/icon_gear.png"))
        QtCore.QTimer.singleShot(100, self.hide_tools_menu)
        # Remove all the actions we added
        self.separator.deleteLater()
        self.show_plus_button.deleteLater()
        self.show_camera_button.deleteLater()
        self.show_light_button.deleteLater()
        self.show_model_button.deleteLater()
        self.show_particle_button.deleteLater()
        self.show_pick_element_button.deleteLater()
        self.show_create_preset_button.deleteLater()
        self.header.deleteLater()
    def hide_tools_menu(self):
        self.tools_menu_shown = False
    def show_plus_button_toggled(self):
        self.settings["show_plus_button"] = not self.settings["show_plus_button"]
        self.save_settings()
        self.apply_settings()
    def show_camera_button_toggled(self):
        self.settings["shown_buttons"]["camera"] = not self.settings["shown_buttons"]["camera"]
        self.save_settings()
        self.apply_settings()
    def show_light_button_toggled(self):
        self.settings["shown_buttons"]["light"] = not self.settings["shown_buttons"]["light"]
        self.save_settings()
        self.apply_settings()
    def show_model_button_toggled(self):
        self.settings["shown_buttons"]["model"] = not self.settings["shown_buttons"]["model"]
        self.save_settings()
        self.apply_settings()
    def show_particle_button_toggled(self):
        self.settings["shown_buttons"]["particle"] = not self.settings["shown_buttons"]["particle"]
        self.save_settings()
        self.apply_settings()
    def show_pick_element_button_toggled(self):
        self.settings["shown_buttons"]["pick_element"] = not self.settings["shown_buttons"]["pick_element"]
        self.save_settings()
        self.apply_settings()
    def show_create_preset_button_toggled(self):
        self.settings["shown_buttons"]["create_preset"] = not self.settings["shown_buttons"]["create_preset"]
        self.save_settings()
        self.apply_settings()
    def closeEvent(self, event):
        self.save_settings()
        event.accept()
    def trigger_old_button(self):
        #self.toolbutton_tools_pressed()
        self.tools_button.menu().exec_(self.toolbutton_tools.mapToGlobal(QtCore.QPoint(0, self.toolbutton_tools.height())))
if __name__ == "__main__":
    extendedExists = globals().get("global_sfmExtended")
    oldEventFilter = globals().get("global_sfmExtended_eventFilter")
    # delete existing instance
    if extendedExists:
        del extendedExists
    if oldEventFilter:
        oldEventFilter.deleteLater()
        globals()["global_sfmExtended_eventFilter"] = None
    sfmExtended = SFMExtended()
    globals()["global_sfmExtended"] = sfmExtended
    globals()["global_sfmExtended_eventFilter"] = sfmExtended.found_event_filter
