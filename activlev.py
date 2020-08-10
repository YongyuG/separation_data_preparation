#Author: Yongyu Gao
#Email : gaoyongyu@cloudwalk.cn

import numpy as np
import scipy.signal
import scipy.sparse
import soundfile as sf

class config:
    def __init__(self, fs):
        self.fs = fs


def poly(x):
    m, n = x.shape
    if m == n:
        e, _ = np.linalg.eig(x)
    elif m==1 or n==1:
        e = x
    else:
        raise ValueError
    e = e[np.isfinite(e)][:,np.newaxis]
    n = len(e)

    c = np.concatenate([np.ones((1,1), dtype=complex), np.zeros((1, n), dtype=complex)],axis=1)

    for j in range(n):
        c[:, 1:j + 2] = c[:, 1:j+2] - e[j] * c[:,:j+1]
    c = c.real
    return c


def gao_log2(x):
    #TODO
    #Need to identify when x = power of 2
    #can use x & x-1 == 0

    log2Result = np.log2(x)
    qe = np.ceil(log2Result)
    qf = x / np.power(2, qe)
    return qf, qe


def maxfilt(x, f, n, d, x0):
    x = x[:,np.newaxis]
    s = x.shape
    if d == 1:
        y = np.append(x0, x)[:,np.newaxis]
    else:
        raise ValueError
    x0 = [x0]
    nx0 = len(x0)
    s = y.shape
    s1 = s[0]

    n0 = int(max(n, 1))
    nn = n0
    if n0 < np.inf:
        ny0 = min(s1, nn-1)
        ny0 = int(ny0)

    sy0 = [ny0, 1]
    if ny0 <= 0 or n0 == np.inf:
        y0 = np.zeros(sy0.shape)
    else:
        y0 = np.reshape(y[s1-ny0:,:].copy(), sy0)
        y0, _ = shiftdim(y0, len(x.shape) - d + 1)

    nn = min(nn, s1)
    temp = np.array([i for i in range(s1)])
    k = np.tile(temp, [1, s[1]]).T

    if nn > 1:
        j = 1
        j2 = 1
        while j > 0:
            g = pow(f, j)
            m = np.where(y[j:s1+1,:]<=g*y[0:s1-j,:])
            newm = m[0] + j * np.fix((m[0]-1)/(s1-j))
            newm = newm.astype(np.int)
            y[newm + j] = g * y[newm]
            k[newm + j] = k[newm]
            j2 = j2 + j
            j = min(j2, nn - j2)

    if nx0 > 0:
        outS = s[0] - nx0
        y, _ = shiftdim(np.reshape(y[nx0:,:], outS), len(x.shape) -d + 1)
        k, _ = shiftdim(np.reshape(k[nx0:,:], outS), len(x.shape) -d + 1)
        k = k - nx0

    return y, k, y0


def rem(x, y):
    return x - y * np.fix(x / y)


def shiftdim(x, n):
    siz = x.shape
    if n > 0:
        n = int(rem(n, len(x.shape)))
    else:
        raise ValueError
    nshift = n
    if n == 0:
        b = x
        nshift = 0
    elif n > 0:
        pass
        #b = np.transpose(x, (n:len(x.shape),:n))
    return b, nshift


def activlev(signal, fs, mode='n'):
    nbin = 20
    thresh = 15.9

    c25zp = [[0 , 0.37843443673309j, 0.23388534441447j, -0.37843443673309j, -0.23388534441447j], [-0.66793268833792, -0.20640255179496 + 0.73942185906851j,
            -0.54036889596392+ 0.45698784092898j, -0.20640255179496 - 0.73942185906851j, -0.54036889596392 - 0.45698784092898j]]
    c25zp = np.array(c25zp, dtype=np.complex)
    configs = config(fs)

    ti = 1 / fs
    g = np.exp(-ti / 0.03)
    configs.ae = np.array([1, -2*g, pow(g,2)]) / pow((1-g), 2)
    configs.ze = np.zeros(2)
    configs.nh = np.ceil(0.2 / ti) + 1
    configs.zx = -np.inf
    configs.emax = -np.inf
    configs.ns = 0
    configs.ssq = 0
    configs.ss = 0
    configs.kc = np.zeros((nbin, 1))

    if mode != '1' and mode != 'e':
        szp = c25zp
    else:
        #TODO
        raise ValueError

    flh = np.array([200, 5500])
    configs.fmd = 'n'

    if mode != '0':
        zl = np.divide(2, 1-szp*np.tan(flh[0]*np.pi/fs))-1
        abl = np.real(np.concatenate((np.ones([2,1]),
                                      -zl[:,0][:, np.newaxis],
                                      -2*np.real(zl[:,1:3]),
                                      pow(np.abs(zl[:, 1:3]),2)), axis=1))

        hfg = np.dot(abl,np.array([1, -1, 0, 0, 0, 0]).T) * \
              np.dot(abl,np.array([1, 0, -1, 0, 1, 0]).T) * \
              np.dot(abl,np.array([1, 0, 0, -1, 0, 1]).T)

        abl = np.concatenate([abl[:,0:2],
                              abl[:,0][:, np.newaxis],
                              abl[:,2][:, np.newaxis],
                              abl[:,-2][:, np.newaxis],
                              abl[:,0][:, np.newaxis],
                              abl[:,3][:, np.newaxis],
                              abl[:,-1][:, np.newaxis]],axis=1)

        abl[0, :2] = abl[0, :2] * hfg[1] / hfg[0]
        configs.abl = abl
        configs.zl = np.zeros((5))

    if mode != 'h':
        zh = np.divide(2, szp/np.tan(flh[1]*np.pi/fs)-1)+1
        ah = poly(zh[1,:][:, np.newaxis])
        bh = poly(zh[0,:][:, np.newaxis])
        configs.bh = bh * np.sum(ah) / np.sum(bh)
        configs.ah = ah
        configs.zh = np.zeros((5, 1))

    md = configs.fmd
    nsp = len(signal)

    if mode != 'z':
        nz = np.ceil(0.35 * configs.fs)
        signal = np.concatenate((signal, np.zeros(int(nz))))

    ns = len(signal)
    if ns:
        if md != '0':
            sq, configs.zl[0] = scipy.signal.lfilter(configs.abl[0, :2], configs.abl[1, :2], signal, zi=[configs.zl[0]])
            sq, configs.zl[1:3] = scipy.signal.lfilter(configs.abl[0, 2:5], configs.abl[1, 2:5], sq, zi=np.squeeze(configs.zl[1:3]))
            sq, configs.zl[3:5] = scipy.signal.lfilter(configs.abl[0, 5:8], configs.abl[1, 5:8], sq, zi=np.squeeze(configs.zl[3:5]))
        if md != 'h':
            sq, configs.zh = scipy.signal.lfilter(np.squeeze(configs.bh), np.squeeze(configs.ah), sq, zi=np.squeeze(configs.zh))

        configs.ns = configs.ns + ns
        configs.ss = configs.ss + sum(sq)
        configs.ssq = configs.ssq + sum(sq * sq)

        s, configs.ze = scipy.signal.lfilter([1], configs.ae, np.abs(sq), zi=configs.ze)
        s[np.where(s == 0.0)] = 1e-12
        qf, qe = gao_log2(s*s)
        qe[qf == 0] = -np.inf
        qe, qk, configs.zx = maxfilt(qe, 1, configs.nh, 1, configs.zx)
        oemax = configs.emax
        configs.emax = max(oemax, max(qe) + 1)
        if configs.emax == -np.inf:
            configs.kc[0] = configs.kc[0] + ns
        else:
            qe = configs.emax - qe
            qe = np.minimum(qe, nbin)
            wqe = np.ones((len(qe), 1))
            _kc = scipy.sparse.csr_matrix((np.squeeze(wqe), (qe, np.squeeze(wqe))), shape=[nbin+1,nbin+1]).toarray()
            _kc = _kc[np.nonzero(_kc)]
            kc = np.cumsum(_kc)
            esh = configs.emax - oemax
            if esh < nbin - 1:
                #TODO
                raise ValueError
            else:
                kc[nbin - 1] = kc[nbin - 1] + sum(configs.kc)
            configs.kc = kc

    if configs.ns:
        if configs.ssq > 0:
            aj = 10 * np.log10(configs.ssq * pow(configs.kc, -1))
            cj = 10 * np.log10(2) * (configs.emax - ([i for i in range(1,nbin+1)]) - 1)
            mj = aj.T - cj - thresh
            jj = np.where((mj[:-1]<0) & (mj[1:]>=0))
            if jj == '' or jj == 'None':
                #TODO
                raise ValueError
            else:
                jf = 1 / (1 - mj[jj[0]+1] / mj[jj[0]])
            lev = aj[jj[0]] + jf * (aj[jj[0] + 1 ] - aj[jj[0]])
            lp = pow(10, lev / 10)
            if md == 'd':
                #TODO
                raise ValueError
            else:
                lev = np.append(lp, configs.ssq/configs.ns)
            af = configs.ssq / (configs.ns * lp)
            if md != 'l':
                lev = lev[0]

    if md == 'n' or md == 'N':
        fso = af
        af = lev

        if md == 'n':
            sq = signal
        if configs.ns > 0 and configs.ssq > 0:
            lev = sq[:nsp] / np.sqrt(lp)
        else:
            lev = sq[:nsp]
    return lev, af



# def main():
#     dataPath = '/home/yongyug/data/timit/TIMIT/TRAIN/DR1/MTRR0/SX108.WAV'
#     data, fs = sf.read(dataPath)
#
#     activlev(data, fs,'n')
#
# main()