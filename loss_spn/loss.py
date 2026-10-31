import torch
from torch import nn


class L1Loss(nn.Module):
    def __init__(self, args):
        super(L1Loss, self).__init__()

        self.args = args
        self.t_valid = 0.0001

    def forward(self, pred, gt):
        # gt = torch.clamp(gt, min=0, max=self.args.max_depth)
        # pred = torch.clamp(pred, min=0, max=self.args.max_depth)

        # mask = (gt > self.t_valid).type_as(pred).detach()

        # d = torch.abs(pred - gt) * mask
        d = torch.abs(pred - gt)

        d = torch.sum(d, dim=[1, 2, 3])
        # num_valid = torch.sum(mask, dim=[1, 2, 3])

        num_valid = torch.sum(torch.ones_like(pred).cuda(), dim=[1, 2, 3])
        loss = d / (num_valid + 1e-8)

        loss = loss.sum()

        return loss


class L2Loss(nn.Module):
    def __init__(self, args):
        super(L2Loss, self).__init__()

        self.args = args
        self.t_valid = 0.0001

    def forward(self, pred, gt):
        # gt = torch.clamp(gt, min=0, max=self.args.max_depth)
        # pred = torch.clamp(pred, min=0, max=self.args.max_depth)

        # mask = (gt > self.t_valid).type_as(pred).detach()

        # d = torch.pow(pred - gt, 2) * mask
        d = torch.pow(pred - gt, 2)

        d = torch.sum(d, dim=[1, 2, 3])
        # num_valid = torch.sum(mask, dim=[1, 2, 3])

        num_valid = torch.sum(torch.ones_like(pred).cuda(), dim=[1, 2, 3])
        loss = d / (num_valid + 1e-8)

        loss = loss.sum()

        return loss


class loss(nn.Module):
    def __init__(self, args):
        super(loss, self).__init__()
        self.args = args
        self.l1_loss = L1Loss(args)
        self.l2_loss = L1Loss(args)

    def forward(self, pred, gt):
        return self.l1_loss(pred, gt)+self.l2_loss(pred, gt)


if __name__ == '__main__':

    l = loss('sss')
    a = torch.randn((1, 3, 32, 32))
    b = torch.randn((1, 3, 32, 32))
    print(l(a, b))