# -*- coding: utf-8 -*-
from collections import namedtuple
from typing import Tuple

import numpy
import yaml
import pandas as pd
import cftime

from bmipy import Bmi

from nwm import NwmHs

BmiVar = namedtuple(
    "BmiVar", ["dtype", "itemsize", "nbytes", "units", "location", "grid"]
)
BmiGridUniformRectilinear = namedtuple(
    "BmiGridUniformRectilinear", ["shape", "yx_spacing", "yx_of_lower_left"]
)


class BmiNwmHs(Bmi):
    def finalize(self) -> None:  # TODO: not sure
        """Perform tear-down tasks for the model.
        Perform all tasks that take place after exiting the model's time
        loop. This typically includes deallocating memory, closing files and
        printing reports.
        """
        self._time_index = 0

    def get_component_name(self) -> str:
        """Name of the component.
        Returns
        -------
        str
            The name of the component.
        """
        return "National Water Model (NWM)"

    def get_current_time(self) -> float:
        """Current time of the model.
        Returns
        -------
        float
            The current model time.
        """
        return float(self._cftime_array[self._time_index])

    def get_end_time(self) -> float:
        """End time of the model.
        Returns
        -------
        float
            The maximum model time.
        """
        return float(self._cftime_array[-1])

    def get_grid_face_edges(self, grid: int, face_edges: numpy.ndarray) -> numpy.ndarray:
        """Get the face-edge connectivity.

        Parameters
        ----------
        grid : int
            A grid identifier.
        face_edges : ndarray of int
            A numpy array to place the face-edge connectivity.

        Returns
        -------
        ndarray of int
            The input numpy array that holds the face-edge connectivity.
        """
        raise NotImplementedError("get_grid_face_edges")

    def get_grid_edge_count(self, grid: int) -> int:
        """Get the number of edges in the grid.
        Parameters
        ----------
        grid : int
            A grid identifier.
        Returns
        -------
        int
            The total number of grid edges.
        """
        raise NotImplementedError("get_grid_edge_count")

    def get_grid_edge_nodes(
        self, grid: int, edge_nodes: numpy.ndarray
    ) -> numpy.ndarray:
        """Get the edge-node connectivity.
        Parameters
        ----------
        grid : int
            A grid identifier.
        edge_nodes : ndarray of int, shape *(2 x nnodes,)*
            A numpy array to place the edge-node connectivity. For each edge,
            connectivity is given as node at edge tail, followed by node at
            edge head.
        Returns
        -------
        ndarray of int
            The input numpy array that holds the edge-node connectivity.
        """
        raise NotImplementedError("get_grid_edge_nodes")

    def get_grid_face_count(self, grid: int) -> int:
        """Get the number of faces in the grid.
        Parameters
        ----------
        grid : int
            A grid identifier.
        Returns
        -------
        int
            The total number of grid faces.
        """
        raise NotImplementedError("get_grid_face_count")

    def get_grid_face_nodes(
        self, grid: int, face_nodes: numpy.ndarray
    ) -> numpy.ndarray:
        """Get the face-node connectivity.
        Parameters
        ----------
        grid : int
            A grid identifier.
        face_nodes : ndarray of int
            A numpy array to place the face-node connectivity. For each face,
            the nodes (listed in a counter-clockwise direction) that form the
            boundary of the face.
        Returns
        -------
        ndarray of int
            The input numpy array that holds the face-node connectivity.
        """
        raise NotImplementedError("get_grid_face_nodes")

    def get_grid_node_count(self, grid: int) -> int:
        """Get the number of nodes in the grid.
        Parameters
        ----------
        grid : int
            A grid identifier.
        Returns
        -------
        int
            The total number of grid nodes.
        """
        raise NotImplementedError("get_grid_node_count")

    def get_grid_nodes_per_face(
        self, grid: int, nodes_per_face: numpy.ndarray
    ) -> numpy.ndarray:
        """Get the number of nodes for each face.
        Parameters
        ----------
        grid : int
            A grid identifier.
        nodes_per_face : ndarray of int, shape *(nfaces,)*
            A numpy array to place the number of edges per face.
        Returns
        -------
        ndarray of int
            The input numpy array that holds the number of nodes per edge.
        """
        raise NotImplementedError("get_grid_nodes_per_face")

    def get_grid_origin(self, grid: int, origin: numpy.ndarray) -> numpy.ndarray:
        """Get coordinates for the lower-left corner of the computational grid.
        Parameters
        ----------
        grid : int
            A grid identifier.
        origin : ndarray of float, shape *(ndim,)*
            A numpy array to hold the coordinates of the lower-left corner of
            the grid.
        Returns
        -------
        ndarray of float
            The input numpy array that holds the coordinates of the grid's
            lower-left corner.
        """
        raise NotImplementedError("get_grid_origin")

    def get_grid_rank(self, grid: int) -> int:
        """Get number of dimensions of the computational grid.
        Parameters
        ----------
        grid : int
            A grid identifier.
        Returns
        -------
        int
            Rank of the grid.
        """
        return 0  # if it is not 1D or 2D grid, it is 0

    def get_grid_shape(self, grid: int, shape: numpy.ndarray) -> numpy.ndarray:
        """Get dimensions of the computational grid.
        Parameters
        ----------
        grid : int
            A grid identifier.
        shape : ndarray of int, shape *(ndim,)*
            A numpy array into which to place the shape of the grid.
        Returns
        -------
        ndarray of int
            The input numpy array that holds the grid's shape.
        """

        raise NotImplementedError("get_grid_shape")

    def get_grid_size(self, grid: int) -> int:
        """Get the total number of elements in the computational grid.
        Parameters
        ----------
        grid : int
            A grid identifier.
        Returns
        -------
        int
            Size of the grid.
        """
        raise NotImplementedError("get_grid_size")

    def get_grid_spacing(self, grid: int, spacing: numpy.ndarray) -> numpy.ndarray:
        """Get distance between nodes of the computational grid.
        Parameters
        ----------
        grid : int
            A grid identifier.
        spacing : ndarray of float, shape *(ndim,)*
            A numpy array to hold the spacing between grid rows and columns.
        Returns
        -------
        ndarray of float
            The input numpy array that holds the grid's spacing.
        """
        raise NotImplementedError("get_grid_spacing")

    def get_grid_type(self, grid: int) -> str:
        """Get the grid type as a string.
        Parameters
        ----------
        grid : int
            A grid identifier.
        Returns
        -------
        str
            Type of grid as a string.
        """
        return "none"  # there is no grid, so type is none.

    def get_grid_x(self, grid: int, x: numpy.ndarray) -> numpy.ndarray:
        """Get coordinates of grid nodes in the x direction.
        Parameters
        ----------
        grid : int
            A grid identifier.
        x : ndarray of float, shape *(nrows,)*
            A numpy array to hold the x-coordinates of the grid node columns.
        Returns
        -------
        ndarray of float
            The input numpy array that holds the grid's column x-coordinates.
        """
        raise NotImplementedError("get_grid_x")

    def get_grid_y(self, grid: int, y: numpy.ndarray) -> numpy.ndarray:
        """Get coordinates of grid nodes in the y direction.
        Parameters
        ----------
        grid : int
            A grid identifier.
        y : ndarray of float, shape *(ncols,)*
            A numpy array to hold the y-coordinates of the grid node rows.
        Returns
        -------
        ndarray of float
            The input numpy array that holds the grid's row y-coordinates.
        """
        raise NotImplementedError("get_grid_y")

    def get_grid_z(self, grid: int, z: numpy.ndarray) -> numpy.ndarray:
        """Get coordinates of grid nodes in the z direction.
        Parameters
        ----------
        grid : int
            A grid identifier.
        z : ndarray of float, shape *(nlayers,)*
            A numpy array to hold the z-coordinates of the grid nodes layers.
        Returns
        -------
        ndarray of float
            The input numpy array that holds the grid's layer z-coordinates.
        """
        raise NotImplementedError("get_grid_z")

    def get_input_var_names(self) -> Tuple[str]:
        """List of a model's input variables.
        Input variable names must be CSDMS Standard Names, also known
        as *long variable names*.
        Returns
        -------
        list of str
            The input variables for the model.
        Notes
        -----
        Standard Names enable the CSDMS framework to determine whether
        an input variable in one model is equivalent to, or compatible
        with, an output variable in another model. This allows the
        framework to automatically connect components.
        Standard Names do not have to be used within the model.
        """
        return self._input_var_names

    def get_input_item_count(self) -> int:
        """Count of a model's input variables.

        Returns
        -------
        int
          The number of input variables.
        """
        return 0

    def get_output_var_names(self) -> Tuple[str]:
        """List of a model's output variables.
        Output variable names must be CSDMS Standard Names, also known
        as *long variable names*.
        Returns
        -------
        list of str
            The output variables for the model.
        """
        return self._output_var_names

    def get_output_item_count(self) -> int:
        """Count of a model's output variables.

        Returns
        -------
        int
          The number of output variables.
        """
        return 1

    def get_start_time(self) -> float:
        """Start time of the model.
        Model times should be of type float.
        Returns
        -------
        float
            The model start time.
        """
        return float(self._cftime_array[0])  # start model time step

    def get_time_step(self) -> float:
        """Current time step of the model.
        The model time step should be of type float.
        Returns
        -------
        float
            The time step used in model.
        """
        return self._time_step

    def get_time_units(self) -> str:
        """Time units of the model.
        Returns
        -------
        float
            The model time unit; e.g., `days` or `s`.
        Notes
        -----
        CSDMS uses the UDUNITS standard from Unidata.
        """
        return self._cftime_unit

    def get_value(self, name: str, dest: numpy.ndarray) -> numpy.ndarray:
        """Get a copy of values of the given variable.
        This is a getter for the model, used to access the model's
        current state. It returns a *copy* of a model variable, with
        the return type, size and rank dependent on the variable.
        Parameters
        ----------
        name : str
            An input or output variable name, a CSDMS Standard Name.
        dest : ndarray
            A numpy array into which to place the values.
        Returns
        -------
        ndarray
            The same numpy array that was passed as an input buffer.
        """
        # return all the value at current time step, for scalar it is just one value
        dest[:] = self._data.values[self._time_index]

    def get_value_at_indices(
        self, name: str, dest: numpy.ndarray, inds: numpy.ndarray  # TODO: not sure
    ) -> numpy.ndarray:
        """Get values at particular indices.
        Parameters
        ----------
        name : str
            An input or output variable name, a CSDMS Standard Name.
        dest : ndarray
            A numpy array into which to place the values.
        indices : array_like
            The indices into the variable array.
        Returns
        -------
        array_like
            Value of the model variable at the given location.
        """
        # return the value at current time step with given index in 1D or 2D grid. when it is scalar no need for ind
        dest[:] = self._data.values[self._time_index]

    def get_value_ptr(self, name: str) -> numpy.ndarray:  # TODO: difference between get_value()?
        """Get a reference to values of the given variable.
        This is a getter for the model, used to access the model's
        current state. It returns a reference to a model variable,
        with the return type, size and rank dependent on the variable.
        Parameters
        ----------
        name : str
            An input or output variable name, a CSDMS Standard Name.
        Returns
        -------
        array_like
            A reference to a model variable.
        """
        # return a reference of all the value at current time step. mainly for input data. not useful for scalar value
        raise NotImplementedError('get_value_ptr')

    def get_var_grid(self, name: str) -> int:
        """Get grid identifier for the given variable.
        Parameters
        ----------
        name : str
            An input or output variable name, a CSDMS Standard Name.
        Returns
        -------
        int
          The grid identifier.
        """
        # for scalar there is no grid, identifier will be 0.
        # this function starts to check other grid property methods
        # when there is no grid, the only grid property will be get_grid_type() as None.
        return 0

    def get_var_itemsize(self, name: str) -> int:
        """Get memory use for each array element in bytes.
        Parameters
        ----------
        name : str
            An input or output variable name, a CSDMS Standard Name.
        Returns
        -------
        int
            Item size in bytes.
        """
        return self._var[name].itemsize

    def get_var_location(self, name: str) -> str:
        """Get the grid element type that the a given variable is defined on.
        The grid topology can be composed of *nodes*, *edges*, and *faces*.
        *node*
            A point that has a coordinate pair or triplet: the most
            basic element of the topology.
        *edge*
            A line or curve bounded by two *nodes*.
        *face*
            A plane or surface enclosed by a set of edges. In a 2D
            horizontal application one may consider the word “polygon”,
            but in the hierarchy of elements the word “face” is most common.
        Parameters
        ----------
        name : str
            An input or output variable name, a CSDMS Standard Name.
        Returns
        -------
        str
            The grid location on which the variable is defined. Must be one of
            `"node"`, `"edge"`, or `"face"`.
        Notes
        -----
        CSDMS uses the `ugrid conventions`_ to define unstructured grids.
        .. _ugrid conventions: http://ugrid-conventions.github.io/ugrid-conventions
        """
        return self._var[name].location

    def get_var_nbytes(self, name: str) -> int:
        """Get size, in bytes, of the given variable.
        Parameters
        ----------
        name : str
            An input or output variable name, a CSDMS Standard Name.
        Returns
        -------
        int
            The size of the variable, counted in bytes.
        """
        # should be nbytes for current time step value
        return self._var[name].nbytes

    def get_var_type(self, name: str) -> str:
        """Get data type of the given variable.
        Parameters
        ----------
        name : str
            An input or output variable name, a CSDMS Standard Name.
        Returns
        -------
        str
            The Python variable type; e.g., ``str``, ``int``, ``float``.
        """
        return self._var[name].dtype

    def get_var_units(self, name: str) -> str:
        """Get units of the given variable.
        Standard unit names, in lower case, should be used, such as
        ``meters`` or ``seconds``. Standard abbreviations, like ``m`` for
        meters, are also supported. For variables with compound units,
        each unit name is separated by a single space, with exponents
        other than 1 placed immediately after the name, as in ``m s-1``
        for velocity, ``W m-2`` for an energy flux, or ``km2`` for an
        area.
        Parameters
        ----------
        name : str
            An input or output variable name, a CSDMS Standard Name.
        Returns
        -------
        str
            The variable units.
        Notes
        -----
        CSDMS uses the `UDUNITS`_ standard from Unidata.
        .. _UDUNITS: http://www.unidata.ucar.edu/software/udunits
        """
        return self._var[name].units

    def initialize(self, config_file: str) -> None:
        """Perform startup tasks for the model.
        Perform all tasks that take place before entering the model's time
        loop, including opening files and initializing the model state. Model
        inputs are read from a text-based configuration file, specified by
        `filename`.
        Parameters
        ----------
        config_file : str, optional
            The path to the model configuration file.
        Notes
        -----
        Models should be refactored, if necessary, to use a
        configuration file. CSDMS does not impose any constraint on
        how configuration files are formatted, although YAML is
        recommended. A template of a model's configuration file
        with placeholder values is used by the BMI.
        """
        if config_file:
            with open(config_file, "r") as fp:
                conf = yaml.safe_load(fp).get("nwmhs", {})
        else:
            conf = {}

        self._data = NwmHs().get_data(**conf) if conf else NwmHs().get_data()

        self._output_var_names = tuple([self._data.variable_name])
        self._input_var_names = ()

        self._grid = {}  # there is no grid

        self._time_index = 0
        time_array = pd.to_datetime(numpy.datetime_as_string(self._data['time'])).to_pydatetime()
        self._cftime_unit = 'seconds since 1970-01-01 00:00:00 UTC'
        self._cftime_array = cftime.date2num(time_array, self._cftime_unit)
        if len(self._cftime_array) > 1:
            self._time_step = self._cftime_array[1] - self._cftime_array[0]
        else:
            self._time_step = 0

        self._var = {}
        for name in self._output_var_names:
            array = self._data.values
            self._var[name] = BmiVar(
                dtype=str(array.dtype),
                itemsize=array.itemsize,
                nbytes=array[self._time_index].nbytes,  # nbytes for current time step value, not the whole time series
                units=self._data.attrs["variable_unit"],  # TODO: translate var name into CSDMS standard name
                location="none",  # scalar value has no location on a grid (node, face, edge)
                grid="none",  # there is no grid, grid is none
            )

    def set_value(self, name: str, values: numpy.ndarray) -> None:
        """Specify a new value for a model variable.
        This is the setter for the model, used to change the model's
        current state. It accepts, through *src*, a new value for a
        model variable, with the type, size and rank of *src*
        dependent on the variable.
        Parameters
        ----------
        var_name : str
            An input or output variable name, a CSDMS Standard Name.
        src : array_like
            The new value for the specified variable.
        """
        raise NotImplementedError("set_value")

    def set_value_at_indices(
        self, name: str, inds: numpy.ndarray, src: numpy.ndarray
    ) -> None:
        """Specify a new value for a model variable at particular indices.
        Parameters
        ----------
        var_name : str
            An input or output variable name, a CSDMS Standard Name.
        indices : array_like
            The indices into the variable array.
        src : array_like
            The new value for the specified variable.
        """
        raise NotImplementedError("set_value_at_indices")

    def update(self) -> None:  # TODO: not sure
        """Advance model state by one time step.
        Perform all tasks that take place within one pass through the model's
        time loop. This typically includes incrementing all of the model's
        state variables. If the model's state variables don't change in time,
        then they can be computed by the :func:`initialize` method and this
        method can return with no action.
        """
        self._time_index += 1

    def update_until(self, time: float) -> None:
        """Advance model state until the given time.

        Parameters
        ----------
        time : float
            A model time later than the current model time.
        """
        raise NotImplementedError("update_until")
