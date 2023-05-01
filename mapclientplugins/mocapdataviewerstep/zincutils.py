'''
MAP Client, a program to generate detailed musculoskeletal models for OpenSim.
Copyright (C) 2012  University of Auckland

This file is part of MAP Client. (http://launchpad.net/mapclient)

MAP Client is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

MAP Client is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with MAP Client.  If not, see <http://www.gnu.org/licenses/>..
'''
from PySide6 import QtCore

from cmlibs.zinc.sceneviewerinput import Sceneviewerinput
from cmlibs.zinc.element import Element, Elementbasis
from cmlibs.zinc.field import Field
from cmlibs.zinc.glyph import Glyph
from cmlibs.zinc.scenecoordinatesystem import SCENECOORDINATESYSTEM_LOCAL, \
    SCENECOORDINATESYSTEM_WINDOW_PIXEL_TOP_LEFT

COORDINATE_SYSTEM_LOCAL = SCENECOORDINATESYSTEM_LOCAL
COORDINATE_SYSTEM_WINDOW_PIXEL_TOP_LEFT = SCENECOORDINATESYSTEM_WINDOW_PIXEL_TOP_LEFT

button_map = {QtCore.Qt.MouseButton.LeftButton: Sceneviewerinput.BUTTON_TYPE_LEFT,
              QtCore.Qt.MouseButton.MiddleButton: Sceneviewerinput.BUTTON_TYPE_MIDDLE,
              QtCore.Qt.MouseButton.RightButton: Sceneviewerinput.BUTTON_TYPE_RIGHT}


# Create a modifier map of Qt modifier keys to Zinc modifier keys
def modifier_map(qt_modifiers):
    '''
    Return a Zinc SceneViewerInput modifiers object that is created from
    the Qt modifier flags passed in.
    '''
    modifiers = Sceneviewerinput.MODIFIER_FLAG_NONE
    if qt_modifiers & QtCore.Qt.KeyboardModifier.ShiftModifier:
        modifiers = modifiers | Sceneviewerinput.MODIFIER_FLAG_SHIFT

    return modifiers


def createFiniteElementField(region):
    '''
    Create a finite element field of three dimensions
    called 'coordinates' and set the coordinate type true.
    '''
    field_module = region.getFieldmodule()
    field_module.beginChange()

    # Create a finite element field with 3 components to represent 3 dimensions
    finite_element_field = field_module.createFieldFiniteElement(3)

    # Set the name of the field
    finite_element_field.setName('coordinates')
    # Set the attribute is managed to 1 so the field module will manage the field for us
    finite_element_field.setManaged(True)
    finite_element_field.setTypeCoordinate(True)

    field_module.endChange()

    return finite_element_field


def createStoredStringField(region):
    '''
    Create a finite element field of three dimensions
    called 'coordinates' and set the coordinate type true.
    '''
    field_module = region.getFieldmodule()
    field_module.beginChange()

    stored_string_field = field_module.createFieldStoredString()
    stored_string_field.setName('stored_string')
    stored_string_field.setManaged(True)

    field_module.endChange()

    return stored_string_field


def create1DFiniteElement(finite_element_field, node1, node2):
    # Use a 3D mesh to to create the 3D finite element.
    fieldmodule = finite_element_field.getFieldmodule()
    mesh = fieldmodule.findMeshByDimension(1)
    element_template = mesh.createElementtemplate()
    element_template.setElementShapeType(Element.SHAPE_TYPE_LINE)
    element_node_count = 2
    element_template.setNumberOfNodes(element_node_count)
    # Specify the dimension and the interpolation function for the element basis function
    linear_basis = fieldmodule.createElementbasis(1, Elementbasis.FUNCTION_TYPE_LINEAR_LAGRANGE)
    # the indecies of the nodes in the node template we want to use.
    node_indexes = [1, 2]

    # Define a nodally interpolated element field or field component in the
    # element_template
    element_template.defineFieldSimpleNodal(finite_element_field, -1, linear_basis, node_indexes)
    element_template.setNode(1, node1)
    element_template.setNode(2, node2)

    element = mesh.createElement(-1, element_template)

    return element


def create3DFiniteElement(fieldmodule, finite_element_field, node_coordinate_set):
    '''
    Create a single finite element using the supplied 
    finite element field and node coordinate set.
    '''
    # Find a special node set named 'nodes'
    nodeset = fieldmodule.findNodesetByName('nodes')
    node_template = nodeset.createNodetemplate()

    # Set the finite element coordinate field for the nodes to use
    node_template.defineField(finite_element_field)
    field_cache = fieldmodule.createFieldcache()

    node_identifiers = []
    # Create eight nodes to define a cube finite element
    for node_coordinate in node_coordinate_set:
        node = nodeset.createNode(-1, node_template)
        node_identifiers.append(node.getIdentifier())
        # Set the node coordinates, first set the field cache to use the current node
        field_cache.setNode(node)
        # Pass in floats as an array
        finite_element_field.assignReal(field_cache, node_coordinate)

    # Use a 3D mesh to to create the 3D finite element.
    mesh = fieldmodule.findMeshByDimension(3)
    element_template = mesh.createElementtemplate()
    element_template.setElementShapeType(Element.SHAPE_TYPE_CUBE)
    element_node_count = 8
    element_template.setNumberOfNodes(element_node_count)
    # Specify the dimension and the interpolation function for the element basis function
    linear_basis = fieldmodule.createElementbasis(3, Elementbasis.FUNCTION_TYPE_LINEAR_LAGRANGE)
    # the indecies of the nodes in the node template we want to use.
    node_indexes = [1, 2, 3, 4, 5, 6, 7, 8]

    # Define a nodally interpolated element field or field component in the
    # element_template
    element_template.defineFieldSimpleNodal(finite_element_field, -1, linear_basis, node_indexes)

    for i, node_identifier in enumerate(node_identifiers):
        node = nodeset.findNodeByIdentifier(node_identifier)
        element_template.setNode(i + 1, node)

    mesh.defineElement(-1, element_template)


def createFiniteElement(region, finite_element_field, dim):
    '''
    Create finite element meshes using the supplied
    finite element field (of three dimensions) and dim list
    of size 3.  The dimension list is the maximum value for a 
    particular dimension.  The origin of the element is set
    at [0, 0, 0].
    '''
    fieldmodule = region.getFieldmodule()
    fieldmodule.beginChange()
    # Define the coordinates for each 3D element
    node_coordinate_set = [[0, 0, 0], [dim[0], 0, 0], [0, dim[1], 0], [dim[0], dim[1], 0], [0, 0, dim[2]],
                           [dim[0], 0, dim[2]], [0, dim[1], dim[2]], [dim[0], dim[1], dim[2]]]
    #         node_coordinate_set = [[-0.5, -0.5, -0.5], [dim[0] + 0.5, -0.5, -0.5], [-0.5, dim[1] + 0.5, -0.5], [dim[0] + 0.5, dim[1] + 0.5, -0.5],
    #                                 [-0.5, -0.5, dim[2] + 0.5], [dim[0] + 0.5, -0.5, dim[2] + 0.5], [-0.5, dim[1] + 0.5, dim[2] + 0.5], [dim[0] + 0.5, dim[1] + 0.5, dim[2] + 0.5]]
    create3DFiniteElement(fieldmodule, finite_element_field, node_coordinate_set)

    fieldmodule.defineAllFaces()
    fieldmodule.endChange()


def createSelectionBox(region, name):
    scene = region.getScene()
    fm = region.getFieldmodule()
    zero_field = fm.createFieldConstant([0, 0, 0])

    scene.beginChange()
    selection_box = scene.createGraphicsPoints()
    selection_box.setName(name)
    selection_box.setCoordinateField(zero_field)
    selection_box.setScenecoordinatesystem(SCENECOORDINATESYSTEM_WINDOW_PIXEL_TOP_LEFT)
    attributes = selection_box.getGraphicspointattributes()
    attributes.setGlyphShapeType(Glyph.SHAPE_TYPE_CUBE_WIREFRAME)
    attributes.setBaseSize([10, 10, 0.9999])

    selection_box.setVisibilityFlag(False)
    scene.endChange()

    return selection_box


def createNodeGraphics(region):
    scene = region.getScene()

    scene.beginChange()
    # Create transparent purple sphere

    materialmodule = scene.getMaterialmodule()
    brown_material = materialmodule.findMaterialByName('brown')
    yellow_material = materialmodule.findMaterialByName('yellow')

    node_graphics = scene.createGraphicsPoints()
    node_graphics.setFieldDomainType(Field.DOMAIN_TYPE_NODES)
    node_graphics_2 = scene.createGraphicsPoints()
    node_graphics_2.setFieldDomainType(Field.DOMAIN_TYPE_NODES)

    fm = region.getFieldmodule()
    coordinate_field = fm.findFieldByName('coordinates')
    node_graphics.setCoordinateField(coordinate_field)
    node_graphics_2.setCoordinateField(coordinate_field)
    node_graphics.setMaterial(brown_material)
    node_graphics.setSelectedMaterial(brown_material)
    node_graphics_2.setSelectedMaterial(yellow_material)

    attributes = node_graphics.getGraphicspointattributes()
    attributes.setGlyphShapeType(Glyph.SHAPE_TYPE_SPHERE)
    attributes.setBaseSize(10)

    attributes = node_graphics_2.getGraphicspointattributes()
    string_field = fm.findFieldByName('stored_string')
    attributes.setLabelField(string_field)
    attributes.setBaseSize(10)
    attributes.setLabelOffset([1.05, 0, 0])

    scene.endChange()

    return [node_graphics, node_graphics_2]
