# -*- coding: utf-8 -*- #
# Copyright 2018 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Update network endpoint group command."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.api_lib.compute import base_classes
from googlecloudsdk.api_lib.compute import network_endpoint_groups
from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.compute import flags as compute_flags
from googlecloudsdk.command_lib.compute.network_endpoint_groups import flags


@base.ReleaseTracks(base.ReleaseTrack.BETA, base.ReleaseTrack.GA)
class Update(base.UpdateCommand):
  r"""Update a Google Compute Engine network endpoint group.

  ## EXAMPLES

  To add two endpoints to a network endpoint group:

    $ {command} my-neg --zone=us-central1-a \
      --add-endpoint=instance=my-instance1,ip=127.0.0.1,port=1234 \
      --add-endpoint=instance=my-instance2

  To remove two endpoints from a network endpoint group:

    $ {command} my-neg --zone=us-central1-a \
      --remove-endpoint=instance=my-instance1,ip=127.0.0.1,port=1234 \
      --remove-endpoint=instance=my-instance2
  """

  @staticmethod
  def Args(parser):
    flags.MakeNetworkEndpointGroupsArg().AddArgument(parser)
    flags.AddUpdateNegArgsToParser(parser)

  def Run(self, args):
    return self._Run(args)

  def _Run(self, args, support_global_scope=False):
    holder = base_classes.ComputeApiHolder(self.ReleaseTrack())
    client = holder.client
    messages = holder.client.messages
    resources = holder.resources

    neg_ref = flags.MakeNetworkEndpointGroupsArg(
        support_global_scope=support_global_scope).ResolveAsResource(
            args,
            resources,
            scope_lister=compute_flags.GetDefaultScopeLister(holder.client))

    client = network_endpoint_groups.NetworkEndpointGroupsClient(client,
                                                                 messages,
                                                                 resources)
    add_endpoints = (
        args.add_endpoint if args.IsSpecified('add_endpoint') else None)
    remove_endpoints = (
        args.remove_endpoint if args.IsSpecified('remove_endpoint') else None)
    return client.Update(
        neg_ref, add_endpoints=add_endpoints, remove_endpoints=remove_endpoints)


@base.ReleaseTracks(base.ReleaseTrack.ALPHA)
class AlphaUpdate(Update):
  r"""Update a Google Compute Engine network endpoint group.

  ## EXAMPLES

  To add two endpoints to a network endpoint group:

    $ {command} my-neg --zone=us-central1-a \
      --add-endpoint=instance=my-instance1,ip=127.0.0.1,port=1234 \
      --add-endpoint=instance=my-instance2

  To remove two endpoints from a network endpoint group:

    $ {command} my-neg --zone=us-central1-a \
      --remove-endpoint=instance=my-instance1,ip=127.0.0.1,port=1234 \
      --remove-endpoint=instance=my-instance2
  """

  @staticmethod
  def Args(parser):
    flags.MakeNetworkEndpointGroupsArg(
        support_global_scope=True).AddArgument(parser)
    flags.AddUpdateNegArgsToParser(
        parser,
        support_global_scope=True,
        support_hybrid_neg=True,
        support_l4ilb_neg=True)

  def Run(self, args):
    return self._Run(args, support_global_scope=True)
