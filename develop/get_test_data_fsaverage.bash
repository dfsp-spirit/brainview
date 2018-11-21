#!/bin/bash
## get_test_data_fsaverage.bash -- Retrieves the fsaverage minimal test data from the internet or a local FreeSurfer installation.
##
## author: Tim Schäfer
## This file is part of brainload. Copright Tim Schäfer, 2018. See the LICENSE file for the license.
##
## Note: The data retrieved by this script is part of the FreeSurfer software (see https://surfer.nmr.mgh.harvard.edu/) and falls under FreeSurfer's license.
## See https://github.com/freesurfer/freesurfer/blob/dev/LICENSE or your local copy at $FREESURFER_HOME/LICENSE if you have FreeSurfer installed.
## The license will also be available in the generated data directory when the script has finished.

APPTAG="[TD_FSAVG]"

if [ -z "${BRAINLOAD_TEST_DATA_DIR}" ]; then
    # Check whether we are in correct dir
    if [ ! -d "tests/test_data" ]; then
        echo "${APPTAG} ERROR: Run this script from the repo root or set the environment variable BRAINLOAD_TEST_DATA_DIR."
        exit 1
    else
        BRAINLOAD_TEST_DATA_DIR="tests/test_data"        # This is the level equivalent to SUBJECTS_DIR from FreeSurfer
        echo "${APPTAG} Environment variable BRAINLOAD_TEST_DATA_DIR was not set, assuming '${BRAINLOAD_TEST_DATA_DIR}'."
    fi
else
    echo "${APPTAG} INFO: Environment variable BRAINLOAD_TEST_DATA_DIR is set, using test data dir '${BRAINLOAD_TEST_DATA_DIR}'."
fi

if [ ! -d "${BRAINLOAD_TEST_DATA_DIR}" ]; then
    echo "${APPTAG} ERROR: The test data directory '${BRAINLOAD_TEST_DATA_DIR}' does not exist. Please fix the environment variable BRAINLOAD_TEST_DATA_DIR."
    exit 1
fi

BRAINLOAD_TEST_DATA_DIR_FSAVERAGE="${BRAINLOAD_TEST_DATA_DIR}/fsaverage"
BRAINLOAD_TEST_DATA_DIR_FSAVERAGE_SURF="${BRAINLOAD_TEST_DATA_DIR_FSAVERAGE}/surf"
MODE="local_then_remote"

ARCHIVE_NAME="fsaverage_min.zip"
REMOTE_ZIP_URL="https://github.com/dfsp-spirit/neuroimaging_testdata/raw/master/freesurfer/official/${ARCHIVE_NAME}"



if [ "$1" = "--local-only" ]; then
    MODE="local"
fi

if [ "$1" = "--remote-only" ]; then
    MODE="remote"
fi

DONE_ALREADY="NO"

mkdir -p "${BRAINLOAD_TEST_DATA_DIR_FSAVERAGE_SURF}" || { echo "ERROR: Could not create directory '${BRAINLOAD_TEST_DATA_DIR_FSAVERAGE_SURF}'." ; exit 1; }

if [ "${MODE}" = "local_then_remote" -o "${MODE}" = "local" ]; then

    echo "${APPTAG} Trying to get data from local FreeSurfer installation..."

    if [ -n "${FREESURFER_HOME}" ]; then
        FD="${FREESURFER_HOME}/subjects/fsaverage/surf"

        # Copy the FreeSurfer license (and potentially other meta data files), as the fsaverage data we copy is part of FreeSurfer
        echo "${APPTAG} Copying FreeSurfer license file from '${FREESURFER_HOME}' to '${BRAINLOAD_TEST_DATA_DIR_FSAVERAGE}'."
        for LFILE in LICENSE; do
            cp "${FREESURFER_HOME}/${LFILE}" "${BRAINLOAD_TEST_DATA_DIR_FSAVERAGE_SURF}" && echo "${APPTAG}  * ${LFILE}"
        done

        # Copy only the data we need for testing. The whole fsaverage subject is vast.
        echo "${APPTAG} Copying fsaverage data from '${FD}' to '${BRAINLOAD_TEST_DATA_DIR_FSAVERAGE_SURF}'."
        for TFILE in lh.inflated lh.pial lh.sphere lh.white rh.inflated rh.pial rh.sphere rh.white; do
            cp "${FD}/${TFILE}" "${BRAINLOAD_TEST_DATA_DIR_FSAVERAGE_SURF}" && echo "${APPTAG}  * ${TFILE}"
        done

        DONE_ALREADY="YES" # We should do error checking, really.

    else
        if [ "${MODE}" = "local" ]; then
            echo "${APPTAG} ERROR: Local-only mode selected, but environment variable FREESURFER_HOME not set. Please install and configure FreeSurfer."
        else
            echo "${APPTAG} No local FreeSurfer installation found (Hint: set FREESURFER_HOME properly in case you have one)."
        fi
    fi
fi

if [ "${MODE}" = "local_then_remote" -a ${DONE_ALREADY} = "NO" -o "${MODE}" = "remote" ]; then

    echo "${APPTAG} Trying to download data from remote location '${REMOTE_ZIP_URL}'..."


    if [ -f "${BRAINLOAD_TEST_DATA_DIR}/${ARCHIVE_NAME}" ]; then
        rm "${BRAINLOAD_TEST_DATA_DIR}/${ARCHIVE_NAME}"
    fi

    cd "${BRAINLOAD_TEST_DATA_DIR}" && wget "${REMOTE_ZIP_URL}" && unzip -f -o ${ARCHIVE_NAME} && rm ${ARCHIVE_NAME} && echo "${APPTAG} OK."
fi
