""" Simple Class for a Galaxy
  Likely to be replaced with an external Class
"""

from __future__ import print_function, absolute_import, division, unicode_literals

import pdb

from astropy.coordinates import SkyCoord

from pyigm.utils import lst_to_array

class GalaxySample(object):
    """A simple object to hold a set of Galaxy Classes

    Parameters
    ----------
    radec : tuple or SkyCoord
      (RA,DEC) in deg or astropy.coordinate
    z : float, optional
      Redshift

    Attributes
    ----------
    name : str
        Name(s)
    z : float, optional
       Adopted redshift
    coord : SkyCoord
    """

    def __init__(self, sample='', ref='', **kwargs):
        """
        Parameters
        ----------
        survey : str, optional
        ref : str, optional

        Returns
        -------

        """
        # Name of survey
        self.sample = sample
        self.ref = ref

        self.galaxies = []
        self.mask = None

    def __getattr__(self, k):
        # Try Self first
        try:
            lst = [getattr(galaxy, k) for galaxy in self.galaxies]
        except AttributeError:
            pdb.set_trace()
            # Galaxy?
            try:
                lst = [getattr(cgm_abs.galaxy, k) for cgm_abs in self.cgm_abs]
            except AttributeError:
                # Try AbsLine_Sys last
                try:
                    lst = [getattr(cgm_abs.igm_sys, k) for cgm_abs in self.cgm_abs]
                except AttributeError:
                    print('cgm.core: Attribute not found!')
                    pdb.set_trace()
        # Special cases
        if k == 'coord':
            ra = [coord.ra.value for coord in lst]
            dec = [coord.dec.value for coord in lst]
            lst = SkyCoord(ra=ra, dec=dec, unit='deg')
            return lst[self.mask]
        # Return array
        return lst_to_array(lst, mask=self.mask)
