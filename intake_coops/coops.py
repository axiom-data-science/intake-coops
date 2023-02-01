from intake.source import base
import pandas as pd
import noaa_coops as nc


class COOPSDataframeSource(base.DataSource):
    """
    platform2 only
    
    Parameters
    ----------
    dataset_id: str
    variables: list

    Returns
    -------
    Dataframe
    """
    name = 'coops-dataframe'
    version = '0.0.1'
    container = 'dataframe'
    partition_access = True
    
    
    def __init__(self, stationid, metadata={}):

        self._dataframe = None
        self.stationid = stationid
        # self.metadata = metadata
        self.s = nc.Station(self.stationid)

        super(COOPSDataframeSource, self).__init__(metadata=metadata)

    def _get_schema(self) -> base.Schema:
        if self._dataframe is None:
            # TODO: could do partial read with chunksize to get likely schema from
            # first few records, rather than loading the whole thing
            self._load()
            self._dataset_metadata = self._get_dataset_metadata()
        # make type checker happy
        assert self._dataframe is not None
        return base.Schema(
            datashape=None,
            dtype=self._dataframe.dtypes,
            shape=self._dataframe.shape,
            npartitions=1,
            extra_metadata=self._dataset_metadata,
        )

    def _get_partition(self) -> pd.DataFrame:
        if self._dataframe is None:
            self._load_metadata()
        return self._dataframe

    def read(self) -> pd.DataFrame:
        """Return the dataframe from ERDDAP"""
        return self._get_partition()

    def _load(self):
        """How to load in a specific station once you know it by dataset_id"""
        
        begin_date = pd.Timestamp(self.s.deployed).strftime("%Y%m%d")
        end_date = pd.Timestamp(self.s.retrieved).strftime("%Y%m%d")
        
        dfs = []
        for bin in self.s.bins["bins"]:
            depth = bin["depth"]
            num = bin["num"]
            df = self.s.get_data(begin_date=begin_date, end_date=end_date, product="currents", bin_num=num)
            df['depth'] = depth
            dfs.append(df)
        self._dataframe = pd.concat(dfs)        
    
    def _get_dataset_metadata(self):
        # self._load()
        # metadata = {}
        metadata = self.s.deployments
        metadata.update(self.s.lat_lon)
        metadata.update({"name": self.s.name, "observe_dst": self.s.observe_dst, "project": self.s.project,
                         "project_type": self.s.project_type, "timezone_offset": self.s.timezone_offset,
                         "units": self.s.units})
        return metadata

    def _close(self):
        self._dataframe = None


class COOPSXarraySource(COOPSDataframeSource):
    """
    platform2 only
    
    Parameters
    ----------
    dataset_id: str
    variables: list

    Returns
    -------
    Dataframe
    """
    name = 'coops-xarray'
    version = '0.0.1'
    container = 'xarray'
    partition_access = True
    
    
    def __init__(self, stationid, metadata={}):

        self._ds = None
        # self.stationid = stationid
        # self.metadata = metadata
        
        self.source = COOPSDataframeSource(stationid, metadata)
        
        
        # self.s = nc.Station(self.stationid)

        super(COOPSXarraySource, self).__init__(stationid=stationid, metadata=metadata)


    def _load(self):
        inds = ['date_time', 'depth']
        df = self.source.read()
        self._ds = df.reset_index().set_index(inds).sort_index().pivot_table(index=inds).to_xarray()

    def read(self):
        if self._ds is None:
            # self._load_metadata()
            self._load()
        return self._ds

    def _close(self):
        self._ds = None
        self._schema = None
