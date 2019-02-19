#!/usr/bin/python3
#
# Copyright (C) 2019 Google Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pandas as pd, numpy as np


class OuterModel:

    def __init__(self, data: pd.DataFrame, y: pd.DataFrame, weights: dict, odm: pd.DataFrame, r_squared: pd.Series):
        self.__crossloadings = y.apply(lambda s: data.corrwith(s))
        loading = (self.__crossloadings * odm).sum(axis=1).to_frame(name="loading")
        communality = loading.apply(lambda s: pow(s, 2))
        communality.columns = ["communality"]
        r_squared_aux = odm.dot(pd.DataFrame(np.diag(r_squared), index=r_squared.index, columns=r_squared.index)).sum(
            axis=1).to_frame(name="communality")
        redundancy = communality * r_squared_aux
        redundancy.columns = ["redundancy"]
        self.__outer_model = pd.concat([weights, loading, communality, redundancy], axis=1, sort=True)

    def model(self):
        return self.__outer_model

    def crossloadings(self):
        return self.__crossloadings
