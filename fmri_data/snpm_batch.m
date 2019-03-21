% The matlab batch script for non-parametric permutation with SnPM.

% Authors : Qi WANG (qiqi.wang@lis-lab.fr)


resultdir = '/fmri_data';
fwe = 0.05;
Nperm = 1000;

snpm_dirname = sprintf('snpm_batch');
outputdir = sprintf('%s/%s', resultdir, snpm_dirname);
snpmfig = sprintf('%s/%s', outputdir, snpm_dirname);


% List of score maps
splits = [1:39];
files=[];
for split = splits
    input_filename = sprintf('ispa_searchlight_accuracy_split%02dof39', split);
    files = [files; cellstr(sprintf('%s/%s.nii', resultdir, input_filename))];
end

files
job_id = 1;
% Matlab batch script
matlabbatch{job_id}.spm.tools.snpm.des.OneSampT.P = files;
matlabbatch{job_id}.spm.tools.snpm.des.OneSampT.cov = struct('c', {}, 'cname', {});
matlabbatch{job_id}.spm.tools.snpm.des.OneSampT.DesignName = 'MultiSub: One Sample T test on diffs/contrasts';
matlabbatch{job_id}.spm.tools.snpm.des.OneSampT.DesignFile = 'snpm_bch_ui_OneSampT';
matlabbatch{job_id}.spm.tools.snpm.des.OneSampT.dir = {outputdir};% Batch Snpm for several directories in InterTVA experiment Batch script
% that run SnPM permutations on searchlights score maps

resultdir = '/hpc/crise/wang.q/data/Searchlight/data/InterTVA';
fwe = 0.05;
Nperm = 1000;

snpm_dirname = sprintf('snpm_batch');
outputdir = sprintf('%s/%s', resultdir, snpm_dirname);
snpmfig = sprintf('%s/%s', outputdir, snpm_dirname);


% List of score maps
splits = [1:39];
files=[];
for split = splits
    input_filename = sprintf('ispa_searchlight_accuracy_split%02dof39', split);
    files = [files; cellstr(sprintf('%s/results/%s.nii', resultdir, input_filename))];
end

files
job_id = 1;
% Matlab batch script
matlabbatch{job_id}.spm.tools.snpm.des.OneSampT.P = files;
matlabbatch{job_id}.spm.tools.snpm.des.OneSampT.cov = struct('c', {}, 'cname', {});
matlabbatch{job_id}.spm.tools.snpm.des.OneSampT.DesignName = 'MultiSub: One Sample T test on diffs/contrasts';
matlabbatch{job_id}.spm.tools.snpm.des.OneSampT.DesignFile = 'snpm_bch_ui_OneSampT';
matlabbatch{job_id}.spm.tools.snpm.des.OneSampT.dir = {outputdir};
matlabbatch{job_id}.spm.tools.snpm.des.OneSampT.nPerm = Nperm;
matlabbatch{job_id}.spm.tools.snpm.des.OneSampT.vFWHM = [0 0 0];
matlabbatch{job_id}.spm.tools.snpm.des.OneSampT.bVolm = 1;
matlabbatch{job_id}.spm.tools.snpm.des.OneSampT.ST.ST_later = -1;
matlabbatch{job_id}.spm.tools.snpm.des.OneSampT.masking.tm.tm_none = 1;
matlabbatch{job_id}.spm.tools.snpm.des.OneSampT.masking.im = 1;
matlabbatch{job_id}.spm.tools.snpm.des.OneSampT.masking.em = {''};
matlabbatch{job_id}.spm.tools.snpm.des.OneSampT.globalc.g_omit = 1;
matlabbatch{job_id}.spm.tools.snpm.des.OneSampT.globalm.gmsca.gmsca_no = 1;
matlabbatch{job_id}.spm.tools.snpm.des.OneSampT.globalm.glonorm = 1;
job_id = job_id + 1;
matlabbatch{job_id}.spm.tools.snpm.cp.snpmcfg(1) = cfg_dep('MultiSub: One Sample T test on diffs/contrasts: SnPMcfg.mat configuration file', substruct('.','val', '{}',{job_id-1}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','SnPMcfg'));
job_id = job_id + 1;
matlabbatch{job_id}.spm.tools.snpm.inference.SnPMmat(1) = cfg_dep('Compute: SnPM.mat results file', substruct('.','val', '{}',{job_id-1}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','SnPM'));
matlabbatch{job_id}.spm.tools.snpm.inference.Thr.Vox.VoxSig.FWEth = fwe;
matlabbatch{job_id}.spm.tools.snpm.inference.Tsign = 1;
matlabbatch{job_id}.spm.tools.snpm.inference.WriteFiltImg.WF_no = 0;
matlabbatch{job_id}.spm.tools.snpm.inference.Report = 'MIPtable';
job_id = job_id + 1;

matlabbatch{job_id}.spm.util.print.fname = snpmfig;
matlabbatch{job_id}.spm.util.print.fig.fighandle = NaN;
matlabbatch{job_id}.spm.util.print.opts = 'png';
job_id = job_id + 1;

matlabbatch{job_id}.spm.tools.snpm.des.OneSampT.nPerm = Nperm;
matlabbatch{job_id}.spm.tools.snpm.des.OneSampT.vFWHM = [0 0 0];
matlabbatch{job_id}.spm.tools.snpm.des.OneSampT.bVolm = 1;
matlabbatch{job_id}.spm.tools.snpm.des.OneSampT.ST.ST_later = -1;
matlabbatch{job_id}.spm.tools.snpm.des.OneSampT.masking.tm.tm_none = 1;
matlabbatch{job_id}.spm.tools.snpm.des.OneSampT.masking.im = 1;
matlabbatch{job_id}.spm.tools.snpm.des.OneSampT.masking.em = {''};
matlabbatch{job_id}.spm.tools.snpm.des.OneSampT.globalc.g_omit = 1;
matlabbatch{job_id}.spm.tools.snpm.des.OneSampT.globalm.gmsca.gmsca_no = 1;
matlabbatch{job_id}.spm.tools.snpm.des.OneSampT.globalm.glonorm = 1;
job_id = job_id + 1;
matlabbatch{job_id}.spm.tools.snpm.cp.snpmcfg(1) = cfg_dep('MultiSub: One Sample T test on diffs/contrasts: SnPMcfg.mat configuration file', substruct('.','val', '{}',{job_id-1}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','SnPMcfg'));
job_id = job_id + 1;
matlabbatch{job_id}.spm.tools.snpm.inference.SnPMmat(1) = cfg_dep('Compute: SnPM.mat results file', substruct('.','val', '{}',{job_id-1}, '.','val', '{}',{1}, '.','val', '{}',{1}, '.','val', '{}',{1}), substruct('.','SnPM'));
matlabbatch{job_id}.spm.tools.snpm.inference.Thr.Vox.VoxSig.FWEth = fwe;
matlabbatch{job_id}.spm.tools.snpm.inference.Tsign = 1;
matlabbatch{job_id}.spm.tools.snpm.inference.WriteFiltImg.WF_no = 0;
matlabbatch{job_id}.spm.tools.snpm.inference.Report = 'MIPtable';
job_id = job_id + 1;

matlabbatch{job_id}.spm.util.print.fname = snpmfig;
matlabbatch{job_id}.spm.util.print.fig.fighandle = NaN;
matlabbatch{job_id}.spm.util.print.opts = 'png';
job_id = job_id + 1;
