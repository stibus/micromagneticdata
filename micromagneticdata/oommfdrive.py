import ubermagutil as uu

import micromagneticdata as md

from .abstract_drive import AbstractDrive


@uu.inherit_docs
class OOMMFDrive(md.Drive):
    """Drive class for OOMMFDrives (created automatically).

    This class provides utility for the analysis of individual OOMMF drives. It should
    not be created explicitly. Instead, use ``micromagneticdata.Drive`` which
    automatically creates a ``drive`` object of the correct sub-type.

    Parameters
    ----------
    name : str

        System's name.

    number : int

        Drive number.

    dirname : str, optional

        Directory in which system's data is saved. Defults to ``'./'``.

    x : str, optional

        Independent variable column name. Defaults to ``None`` and depending on
        the driver used, one is found automatically.

    Raises
    ------
    IOError

        If the drive directory cannot be found.

    Examples
    --------
    1. Getting drive object.

    >>> import os
    >>> import micromagneticdata as md
    ...
    >>> dirname = dirname=os.path.join(os.path.dirname(__file__),
    ...                                'tests', 'test_sample')
    >>> drive = md.Drive(name='system_name', number=0, dirname=dirname)

    """

    def __init__(self, name, number, dirname="./", x=None, use_cache=False, **kwargs):
        super().__init__(name, number, dirname, x, use_cache, **kwargs)

    @AbstractDrive.x.setter
    def x(self, value):
        if value is None:
            if self.info["driver"] == "TimeDriver":
                self._x = "t"
            elif self.info["driver"] == "MinDriver":
                self._x = "iteration"
            elif self.info["driver"] == "HysteresisDriver":
                self._x = "B_hysteresis"
        else:
            self._x = value
            # self.table reads self.x so self._x has to be defined first
            if value not in self.table.data.columns:
                raise ValueError(f"Column {value=} does not exist in data.")

    @property
    def _table_path(self):
        return self.drive_path / f"{self.name}.odt"

    @property
    def _step_file_glob(self):
        return self.drive_path.glob(f"{self.name}*.omf")

    @property
    def calculator_script(self):
        with (self.drive_path / f"{self.name}.mif").open() as f:
            return f.read()

    def __repr__(self):
        """Representation string.

        Returns
        -------
        str

            Representation string.

        Examples
        --------
        1. Representation string.

        >>> import os
        >>> import micromagneticdata as md
        ...
        >>> dirname = dirname=os.path.join(os.path.dirname(__file__),
        ...                                'tests', 'test_sample')
        >>> drive = md.Drive(name='system_name', number=0, dirname=dirname)
        >>> drive
        OOMMFDrive(name='system_name', number=0, dirname='...test_sample', x='t')

        """
        return (
            f"OOMMFDrive(name='{self.name}', number={self.number}, "
            f"dirname='{self.dirname}', x='{self.x}')"
        )
